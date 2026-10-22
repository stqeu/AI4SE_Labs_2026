"""Deterministic (non-AI) nodes of the network (ANS2).

* loader_node     - reads every supported file under the input directory
* prededup_node   - groups near-duplicate candidates (TF-IDF cosine)
* repair_plan     - makes the Planner's topic assignment complete and sized
                    (used inside planner_node)
* assembler_node  - joins the parallel per-topic Consolidator results
* validator_node  - assigns IDs, derives tracing, checks completeness/schema
* renderer_node   - writes the final Markdown + JSON document

Every node takes the LangGraph state and returns a partial state update.
"""
from __future__ import annotations

import email
import email.policy
import email.utils
import json
import re
from datetime import datetime
from pathlib import Path

from config import SETTINGS
from schemas import (ID_PREFIX, PRIORITY_ORDER, PRIORITY_SCALE, BatchResult,
                     BlacklistEntry, CandidateRequirement, ConsolidationResult,
                     DocType, GlossaryTerm, Issue, IssueType, PlanResult, Priority,
                     Requirement, ReqType, Severity, SourceDocument, Topic)
from similarity import cluster, similar_pairs, top_k_similar
from state import GraphState

# ==========================================================================
# 1. LOADER
# ==========================================================================
_DATE_IN_NAME = re.compile(r"(\d{4}-\d{2}-\d{2})")
_SEPARATOR = re.compile(r"^[\s=\-_*#~]+$")

_TYPE_KEYWORDS: list[tuple[DocType, tuple[str, ...]]] = [
    (DocType.INTERVIEW, ("interview",)),
    (DocType.MEETING_MINUTES, ("minutes", "meeting")),
    (DocType.SURVEY, ("survey", "questionnaire")),
    (DocType.SPECIFICATION, ("srs", "specification", "requirements", "spec")),
    (DocType.REFERENCE, ("reference", "manual", "documentation", "guide")),
]


def _read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _guess_type(path: Path, title: str) -> DocType:
    if path.suffix.lower() == ".eml":
        return DocType.EMAIL
    haystack = f"{path.stem} {title}".lower()
    for doc_type, words in _TYPE_KEYWORDS:
        if any(w in haystack for w in words):
            return doc_type
    return DocType.OTHER


def _first_title_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line and not _SEPARATOR.match(line):
            return line[:120]
    return "(untitled)"


def _parse_email(raw: str) -> tuple[str, str | None, str | None, str]:
    """Return (subject, author, iso_date, body). Threads keep all messages."""
    msg = email.message_from_string(raw, policy=email.policy.default)
    subject = str(msg.get("Subject", "")).strip() or "(no subject)"
    author = str(msg.get("From", "")).strip() or None
    date = None
    if msg.get("Date"):
        try:
            date = email.utils.parsedate_to_datetime(str(msg["Date"])).date().isoformat()
        except (TypeError, ValueError):
            date = None
    try:
        if msg.is_multipart():
            parts = [p.get_content() for p in msg.walk()
                     if p.get_content_type() == "text/plain"]
            body = "\n\n".join(parts)
        else:
            body = msg.get_content()
    except (KeyError, LookupError):
        body = raw.split("\n\n", 1)[-1]
    # keep the header block too: sender/date matter for tracing and context
    header = f"From: {author}\nDate: {msg.get('Date', '')}\nSubject: {subject}\n\n"
    return subject, author, date, header + body.strip()


def chunk_text(text: str, max_chars: int) -> list[str]:
    """Split on paragraph boundaries; one paragraph of overlap between chunks."""
    if len(text) <= max_chars:
        return [text]
    paragraphs = re.split(r"\n\s*\n", text)
    chunks, current = [], []
    size = 0
    for para in paragraphs:
        if current and size + len(para) > max_chars:
            chunks.append("\n\n".join(current))
            current = current[-1:]          # overlap
            size = len(current[0])
        current.append(para)
        size += len(para) + 2
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def load_documents(input_dir: str | Path,
                   suffixes: tuple[str, ...] = SETTINGS.file_suffixes,
                   chunk_chars: int = SETTINGS.chunk_chars) -> list[SourceDocument]:
    root = Path(input_dir).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Input directory not found: {root}")
    files = sorted((p for p in root.rglob("*")
                    if p.is_file() and p.suffix.lower() in suffixes),
                   key=lambda p: p.relative_to(root).as_posix().lower())
    width = max(2, len(str(len(files))))
    docs = []
    for i, path in enumerate(files, start=1):
        raw = _read_text(path)
        if path.suffix.lower() == ".eml":
            title, author, date, text = _parse_email(raw)
        else:
            title, author, text = _first_title_line(raw), None, raw.strip()
            m = _DATE_IN_NAME.search(path.name)
            date = m.group(1) if m else None
        if not text.strip():
            continue
        docs.append(SourceDocument(
            doc_id=f"D{i:0{width}d}",
            path=path.relative_to(root).as_posix(),
            doc_type=_guess_type(path, title),
            title=title, date=date, author=author, text=text,
            chunks=chunk_text(text, chunk_chars),
        ))
    return docs


def loader_node(state: GraphState) -> dict:
    docs = load_documents(state["input_dir"])
    if not docs:
        raise ValueError(f"No {SETTINGS.file_suffixes} files in {state['input_dir']}")
    print(f"[loader] {len(docs)} documents loaded "
          f"({sum(len(d.chunks) for d in docs)} chunks)")
    return {"documents": docs, "round": 0}


# ==========================================================================
# 2. PRE-DEDUP
# ==========================================================================
def candidate_text(c: CandidateRequirement) -> str:
    return f"{c.name}. {c.name}. {c.description}"   # name weighted twice


def prededup_node(state: GraphState) -> dict:
    cands = state.get("candidates", [])
    groups = cluster([candidate_text(c) for c in cands], SETTINGS.dedup_threshold)
    clusters = [[cands[i].cand_id for i in g] for g in groups]
    in_clusters = sum(len(g) for g in clusters)
    print(f"[prededup] {len(cands)} candidates -> {len(clusters)} similarity "
          f"groups covering {in_clusters} candidates")
    return {"clusters": clusters}


# ==========================================================================
# 2b. PLAN REPAIR  (deterministic post-processing of the Planner LLM)
# ==========================================================================
def _title(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    return text[:1].upper() + text[1:] if text else "General"


def fallback_plan(candidates: list[CandidateRequirement]) -> PlanResult:
    """Used only if the Planner LLM fails: one topic per extractor category."""
    from schemas import PlannedTopic
    groups: dict[str, list[str]] = {}
    for c in candidates:
        groups.setdefault(_title(c.category), []).append(c.cand_id)
    return PlanResult(glossary=[], topics=[
        PlannedTopic(name=k, scope=f"Candidates categorised as {k}.", candidate_ids=v)
        for k, v in sorted(groups.items())])


def repair_plan(plan: PlanResult, candidates: list[CandidateRequirement],
                colocate_threshold: float = SETTINGS.colocate_threshold,
                max_batch: int = SETTINGS.max_batch_size,
                min_batch: int = SETTINGS.min_batch_size) -> tuple[list[Topic], dict]:
    """Make the LLM's topic assignment safe to rely on.

    1. drop unknown IDs, keep the first assignment of IDs listed twice,
       merge topics with the same name, drop empty topics;
    2. assign every forgotten candidate to the topic of its most similar
       assigned candidate (completeness, OS8);
    3. keep textual near-duplicates in ONE topic, so the Consolidator can
       merge them (OS3);
    4. merge topics smaller than ``min_batch`` into the most similar topic
       (avoids many tiny, expensive calls);
    5. split topics larger than ``max_batch`` into parts of similar items.
    Returns (topics, stats).
    """
    by_id = {c.cand_id: c for c in candidates}
    stats = {"unknown_ids": 0, "double_assigned": 0, "unassigned": 0, "moved": 0,
             "merged_small_topics": 0, "split_topics": 0}

    # 1. clean
    names: list[str] = []
    scopes: dict[str, str] = {}
    members: dict[str, list[str]] = {}
    owner: dict[str, str] = {}
    for t in plan.topics:
        name = _title(t.name)
        key = name.lower()
        if key not in members:
            names.append(name)
            members[key] = []
            scopes[key] = t.scope.strip()
        for cid in t.candidate_ids:
            if cid not in by_id:
                stats["unknown_ids"] += 1
            elif cid in owner:
                stats["double_assigned"] += 1
            else:
                owner[cid] = key
                members[key].append(cid)

    # 2. forgotten candidates -> topic of the most similar assigned candidate
    assigned = [c for c in candidates if c.cand_id in owner]
    loose = [c for c in candidates if c.cand_id not in owner]
    stats["unassigned"] = len(loose)
    if loose and assigned:
        best = top_k_similar([candidate_text(c) for c in loose],
                             [candidate_text(c) for c in assigned], 1)
        for c, hit in zip(loose, best):
            key = owner[assigned[hit[0][0]].cand_id]
            owner[c.cand_id] = key
            members[key].append(c.cand_id)
    elif loose:                                  # planner assigned nothing at all
        return repair_plan(fallback_plan(candidates), candidates,
                           colocate_threshold, max_batch, min_batch)

    # 3. co-locate near-duplicates in the topic holding most of the group
    groups = cluster([candidate_text(c) for c in candidates], colocate_threshold)
    for g in groups:
        ids = [candidates[i].cand_id for i in g]
        counts: dict[str, int] = {}
        for cid in ids:
            counts[owner[cid]] = counts.get(owner[cid], 0) + 1
        target = max(counts, key=lambda k: (counts[k], -list(members).index(k)))
        for cid in ids:
            if owner[cid] != target:
                members[owner[cid]].remove(cid)
                members[target].append(cid)
                owner[cid] = target
                stats["moved"] += 1

    # 4. merge tiny topics into the most similar remaining topic
    def topic_text(key: str) -> str:
        return " ".join(candidate_text(by_id[i]) for i in members[key])

    while True:
        live = [k for k in members if members[k]]
        small = sorted((k for k in live if len(members[k]) < min_batch),
                       key=lambda k: len(members[k]))
        if not small or len(live) < 2:
            break
        key = small[0]
        targets = [k for k in live if k != key and len(members[k]) >= min_batch] \
            or [k for k in live if k != key]
        best = top_k_similar([topic_text(key)], [topic_text(k) for k in targets], 1)[0]
        target = targets[best[0][0]] if best else targets[0]
        for cid in members[key]:
            owner[cid] = target
        members[target].extend(members[key])
        members[key] = []
        stats["merged_small_topics"] += 1

    # 5. split oversized topics into parts of similar candidates
    group_of = {candidates[i].cand_id: n for n, g in enumerate(groups) for i in g}
    topics: list[Topic] = []
    n = 0
    for name in names:
        key = name.lower()
        ids = members[key]
        if not ids:
            continue
        n += 1
        if len(ids) <= max_batch:
            topics.append(Topic(topic_id=f"T{n:02d}", name=name, scope=scopes[key],
                                candidate_ids=ids))
            continue
        stats["split_topics"] += 1
        # units = near-duplicate groups (kept whole) or single candidates,
        # ordered by extractor category then name so similar items are adjacent
        units: dict[object, list[str]] = {}
        for cid in ids:
            units.setdefault(group_of.get(cid, cid), []).append(cid)
        ordered = sorted(units.values(), key=lambda u: (
            by_id[u[0]].category.lower(), by_id[u[0]].name.lower()))
        n_parts = -(-len(ids) // max_batch)
        target_size = -(-len(ids) // n_parts)
        parts: list[list[str]] = [[]]
        for unit in ordered:
            if parts[-1] and len(parts[-1]) + len(unit) > target_size:
                parts.append([])
            parts[-1].extend(unit)
        while len(parts) > 1 and len(parts[-1]) < min_batch:   # no tiny leftovers
            parts[-2].extend(parts.pop())
        for k, part in enumerate(parts, start=1):
            topics.append(Topic(topic_id=f"T{n:02d}.{k}", name=name,
                                scope=scopes[key], candidate_ids=part))
    return topics, stats


# ==========================================================================
# 2c. ASSEMBLER  (joins the parallel per-topic Consolidator results)
# ==========================================================================
def merge_glossaries(*lists: list[GlossaryTerm]) -> list[GlossaryTerm]:
    out: dict[str, GlossaryTerm] = {}
    for lst in lists:
        for g in lst:
            key = g.term.strip().lower()
            if key in out:
                known = out[key].synonyms_replaced
                out[key].synonyms_replaced = known + [s for s in g.synonyms_replaced
                                                      if s not in known]
            else:
                out[key] = g.model_copy(deep=True)
    return sorted(out.values(), key=lambda g: g.term.lower())


def assemble(batches: list[BatchResult], topics: list[Topic],
             plan_glossary: list[GlossaryTerm]) -> ConsolidationResult:
    topic_ids = {t.topic_id: set(t.candidate_ids) for t in topics}
    reqs, bl, glossaries = [], [], [plan_glossary]
    for b in sorted(batches, key=lambda b: b.topic_id):
        allowed = topic_ids.get(b.topic_id, set())
        for r in b.result.requirements:
            reqs.append(r.model_copy(update={
                "category": b.topic_name,            # consistent sections (OS7)
                "merged_from": [i for i in r.merged_from if i in allowed]}))
        for d in b.result.blacklist:
            bl.append(d.model_copy(update={
                "candidate_ids": [i for i in d.candidate_ids if i in allowed]}))
        glossaries.append(b.result.glossary)
    return ConsolidationResult(glossary=merge_glossaries(*glossaries),
                               requirements=reqs, blacklist=bl)


def assembler_node(state: GraphState) -> dict:
    batches = state.get("batch_results", [])
    result = assemble(batches, state.get("topics", []), state.get("plan_glossary", []))
    print(f"[assembler] {len(batches)} topic batches -> {len(result.requirements)} "
          f"requirements, {len(result.blacklist)} blacklisted, "
          f"{len(result.glossary)} glossary terms")
    return {"consolidation": result}


# ==========================================================================
# 3. VALIDATOR
# ==========================================================================
_TYPE_ORDER = {t: i for i, t in enumerate(ReqType)}


def _norm_category(cat: str) -> str:
    cat = re.sub(r"\s+", " ", cat.strip()) or "General"
    return cat[0].upper() + cat[1:]


# "out_of_scope" is valid only for statements that are not about the software
# (project tasks, meetings, documents, process, chit-chat). A discard explained
# by "belongs to another topic / outside this topic's scope" is not valid.
_WRONG_TOPIC = re.compile(
    r"\b(topic|handled separately|handled (?:by|under|in)|belongs (?:to|in|under)|"
    r"outside (?:the|this) (?:defined )?\w*\s*\w*\s*scope)\b", re.I)
_NOT_SOFTWARE = re.compile(
    r"\b(project|meeting|document(?:ation|-writing)?|srs|methodolog\w*|process|"
    r"task|governance|planning|plan|deliverable|requirements?-gathering|workflow of "
    r"the (?:project|team)|personal|anecdote|chit-chat|greeting|schedule of)\b", re.I)


def _wrong_topic_discard(explanation: str) -> bool:
    return bool(_WRONG_TOPIC.search(explanation)) or not _NOT_SOFTWARE.search(explanation)


def _match_name(name: str | None, reqs: list[Requirement]) -> Requirement | None:
    if not name:
        return None
    key = name.strip().lower()
    for r in reqs:
        if r.name.lower() == key or r.req_id.lower() == key:
            return r
    texts = [name] + [r.name for r in reqs]
    best = [(j, s) for i, j, s in similar_pairs(texts, 0.5) if i == 0]
    return reqs[max(best, key=lambda x: x[1])[0] - 1] if best else None


def validate(consolidation: ConsolidationResult,
             candidates: list[CandidateRequirement],
             documents: list[SourceDocument]):
    """Pure function: returns (requirements, blacklist, issues)."""
    by_id = {c.cand_id: c for c in candidates}
    issues: list[Issue] = []

    def resolve(ids: list[str], owner_id: str, owner_name: str) -> list[str]:
        ids = list(dict.fromkeys(ids))                  # drop repeated IDs
        good = [i for i in ids if i in by_id]
        bad = [i for i in ids if i not in by_id]
        if bad:
            issues.append(Issue(
                issue_type=IssueType.SCHEMA, affected=[owner_id] + bad,
                origin="validator",
                description=f"{owner_id} '{owner_name}' references unknown candidate "
                            f"IDs {bad}.",
                suggested_fix="Use only candidate IDs from the provided list."))
        return good

    def sources_of(ids: list[str]) -> list[str]:
        return sorted({by_id[i].source_doc_id for i in ids})

    # ---- requirements: sort, assign IDs (OS2), derive tracing (OS4) ----
    raw = sorted(consolidation.requirements, key=lambda r: (
        _TYPE_ORDER[r.req_type], _norm_category(r.category).lower(),
        PRIORITY_ORDER[r.priority], r.name.lower()))
    counters: dict[str, int] = {}
    reqs: list[Requirement] = []
    for r in raw:
        prefix = ID_PREFIX[r.req_type]
        counters[prefix] = counters.get(prefix, 0) + 1
        req_id = f"{prefix}-{counters[prefix]:03d}"
        merged = resolve(r.merged_from, req_id, r.name)
        req = Requirement(**{**r.model_dump(), "category": _norm_category(r.category),
                             "merged_from": merged},
                          req_id=req_id, sources=sources_of(merged))
        reqs.append(req)
        if not merged:
            issues.append(Issue(
                issue_type=IssueType.SCHEMA, affected=[req.req_id], origin="validator",
                description=f"{req.req_id} '{req.name}' has no valid source candidates, "
                            "so it cannot be traced to any input document.",
                suggested_fix="List the candidate IDs it was derived from, or drop it."))
        words = len(req.description.split())
        if words < SETTINGS.min_description_words:
            issues.append(Issue(
                issue_type=IssueType.WEAK_DESCRIPTION, affected=[req.req_id],
                origin="validator", severity=Severity.MINOR,
                description=f"{req.req_id} description has only {words} words; "
                            "a paragraph-long explanation is required.",
                suggested_fix="Expand to 3-6 sentences: behaviour, context, intent."))
        if not req.description.lower().startswith("the system shall"):
            issues.append(Issue(
                issue_type=IssueType.TERMINOLOGY, affected=[req.req_id],
                origin="validator", severity=Severity.MINOR,
                description=f"{req.req_id} does not start with 'The system shall'.",
                suggested_fix="Use the standard requirement phrasing."))
        if len(merged) > SETTINGS.too_broad_candidates:
            issues.append(Issue(
                issue_type=IssueType.TOO_BROAD, affected=[req.req_id], origin="validator",
                description=f"{req.req_id} '{req.name}' merges {len(merged)} candidates "
                            f"from {len(req.sources)} documents; it is probably a "
                            "catch-all covering several distinct needs.",
                suggested_fix="Split it into one requirement per distinct, testable "
                              "need; keep merging only true duplicates."))
        if len(req.name.split()) > 10:
            issues.append(Issue(
                issue_type=IssueType.WEAK_DESCRIPTION, affected=[req.req_id],
                origin="validator", severity=Severity.MINOR,
                description=f"{req.req_id} name is too long for a short name.",
                suggested_fix="Shorten the name to 3-8 words."))

    # ---- blacklist (OS9) ----
    blacklist: list[BlacklistEntry] = []
    for k, d in enumerate(consolidation.blacklist, start=1):
        entry_id = f"BL-{k:03d}"
        ids = resolve(d.candidate_ids, entry_id, d.name)
        entry = BlacklistEntry(**{**d.model_dump(), "candidate_ids": ids},
                               entry_id=entry_id, sources=sources_of(ids))
        match = _match_name(d.conflicts_with, reqs)
        if match:
            entry.conflicts_with = f"{match.req_id} ({match.name})"
        blacklist.append(entry)
        if d.reason.value == "out_of_scope" and _wrong_topic_discard(entry.explanation):
            issues.append(Issue(
                issue_type=IssueType.BAD_BLACKLIST, affected=[entry.entry_id] + ids,
                origin="validator",
                description=f"{entry.entry_id} '{entry.name}' is discarded as out of "
                            "scope although it describes the software (it only seems to "
                            "belong to another topic); that is not a valid reason to "
                            "discard a need.",
                suggested_fix="Restore it as a requirement (merge it into an existing "
                              "requirement if it duplicates one)."))
        if len(entry.explanation.split()) < 6:
            issues.append(Issue(
                issue_type=IssueType.BAD_BLACKLIST, affected=[entry.entry_id],
                origin="validator", severity=Severity.MINOR,
                description=f"{entry.entry_id} '{entry.name}' lacks a real explanation.",
                suggested_fix="Explain why it was discarded."))

    # ---- each candidate belongs to exactly one place (OS3) ----
    owners: dict[str, list[str]] = {}
    for r in reqs:
        for i in r.merged_from:
            owners.setdefault(i, []).append(r.req_id)
    for b in blacklist:
        for i in b.candidate_ids:
            owners.setdefault(i, []).append(b.entry_id)
    shared: dict[tuple[str, ...], list[str]] = {}
    for cid, own in owners.items():
        if len(own) > 1:
            shared.setdefault(tuple(own), []).append(cid)
    for own, cids in shared.items():
        kept_and_dropped = any(o.startswith("BL-") for o in own)
        issues.append(Issue(
            issue_type=IssueType.REUSED, affected=list(own) + cids, origin="validator",
            description=(f"Candidate(s) {cids} are used by {', '.join(own)}. "
                         + ("A statement cannot be both kept and discarded."
                            if kept_and_dropped else
                            "Requirements sharing a source statement are probably "
                            "duplicates or overlap.")),
            suggested_fix="Merge the overlapping items, or assign each candidate to "
                          "exactly one requirement or blacklist entry."))

    # ---- completeness (OS8): every candidate must be accounted for ----
    used = {i for r in reqs for i in r.merged_from} | \
           {i for b in blacklist for i in b.candidate_ids}
    missing = [c for c in candidates if c.cand_id not in used]
    if missing:
        listing = "; ".join(f"{c.cand_id} '{c.name}'" for c in missing[:40])
        issues.append(Issue(
            issue_type=IssueType.UNACCOUNTED, affected=[c.cand_id for c in missing],
            origin="validator",
            description=f"{len(missing)} candidate(s) are neither merged into a "
                        f"requirement nor blacklisted: {listing}"
                        + (" ..." if len(missing) > 40 else ""),
            suggested_fix="Merge each into a requirement (add to merged_from), "
                          "create a new requirement, or blacklist it with a reason."))

    # every document should contribute at least one kept requirement
    covered = {s for r in reqs for s in r.sources}
    for doc in documents:
        if doc.doc_id not in covered:
            issues.append(Issue(
                issue_type=IssueType.MISSING, affected=[doc.doc_id], origin="validator",
                severity=Severity.MINOR,
                description=f"No kept requirement traces to {doc.doc_id} ({doc.path}).",
                suggested_fix="Check whether requirements from this document were "
                              "lost or wrongly discarded."))

    # ---- duplicates (OS3) ----
    texts = [f"{r.name}. {r.name}. {r.description}" for r in reqs]
    for i, j, s in similar_pairs(texts, SETTINGS.duplicate_threshold):
        issues.append(Issue(
            issue_type=IssueType.DUPLICATE, affected=[reqs[i].req_id, reqs[j].req_id],
            origin="validator",
            description=f"{reqs[i].req_id} '{reqs[i].name}' and {reqs[j].req_id} "
                        f"'{reqs[j].name}' are textually very similar ({s:.2f}).",
            suggested_fix="Merge them if they mean the same thing."))

    return reqs, blacklist, issues


def validator_node(state: GraphState) -> dict:
    reqs, blacklist, issues = validate(
        state["consolidation"], state.get("candidates", []), state["documents"])
    print(f"[validator] {len(reqs)} requirements, {len(blacklist)} blacklisted, "
          f"{len(issues)} issues")
    return {"requirements": reqs, "blacklist": blacklist,
            "glossary": state["consolidation"].glossary,
            "validation_issues": issues}


# ==========================================================================
# 4. RENDERER
# ==========================================================================
def _md(text: str) -> str:
    """Escape table-breaking characters."""
    return text.replace("|", "\\|").replace("\n", " ").strip()


def render_markdown(state: GraphState) -> str:
    docs = state["documents"]
    reqs = state.get("requirements", [])
    blacklist = state.get("blacklist", [])
    glossary = state.get("glossary", [])
    history = state.get("review_history", [])
    final_review = history[-1] if history else None
    doc_by_id = {d.doc_id: d for d in docs}
    L: list[str] = []
    add = L.append

    add("# Software Requirements Specification")
    add("")
    add(f"*Generated {datetime.now():%Y-%m-%d %H:%M} by the requirements-refinement "
        f"agentic network from `{Path(state['input_dir']).name}/` "
        f"({len(docs)} source documents).*")
    add("")

    # ---- 1. about ----
    add("## 1. About this document")
    add("")
    add("This document consolidates the software requirements stated across the "
        "input corpus. Every requirement has a unique ID, a short name, a "
        "paragraph-long explanation, a priority and a list of the source "
        "documents it was derived from. Semantically duplicate statements were "
        "merged into one requirement; statements discarded as conflicting, "
        "nonsensical or out of scope are listed in the Blacklist (section 8).")
    add("")
    n_types = {t: sum(r.req_type == t for r in reqs) for t in ReqType}
    add("| Metric | Value |")
    add("|---|---|")
    add(f"| Source documents | {len(docs)} |")
    add(f"| Candidate statements extracted | {len(state.get('candidates', []))} |")
    add(f"| Requirements kept | {len(reqs)} "
        f"(FR {n_types[ReqType.FUNCTIONAL]}, NFR {n_types[ReqType.NON_FUNCTIONAL]}, "
        f"CON {n_types[ReqType.CONSTRAINT]}) |")
    add(f"| Blacklisted | {len(blacklist)} |")
    topics = state.get("topics", [])
    if topics:
        add(f"| Topics (planner) | {len({t.name for t in topics})} "
            f"in {len(topics)} consolidation batches |")
    add(f"| Review rounds | {len(history)} |")
    if final_review:
        add(f"| Final review verdict | {'approved' if final_review.approved else 'not approved'} |")
    add(f"| Models | extractor `{SETTINGS.model_extractor}`, planner "
        f"`{SETTINGS.model_planner}`, consolidator/reviser "
        f"`{SETTINGS.model_consolidator}`, reviewer `{SETTINGS.model_reviewer}` |")
    from llm_client import USAGE
    for model, u in sorted(USAGE.by_model.items()):
        add(f"| Tokens `{model}` | {u.calls} calls, {u.prompt_tokens:,} prompt + "
            f"{u.completion_tokens:,} completion |")
    add("")

    # ---- 2. ID scheme + priority scale ----
    add("## 2. Identification and priority scale")
    add("")
    add("**IDs.** `FR-nnn` functional requirement, `NFR-nnn` non-functional "
        "(quality) requirement, `CON-nnn` constraint, `BL-nnn` blacklisted "
        "statement. Source documents are referred to as `Dnn` (section 4).")
    add("")
    add("**Priority (MoSCoW).**")
    add("")
    add("| Priority | Meaning |")
    add("|---|---|")
    for p in Priority:
        add(f"| **{p.value}** | {PRIORITY_SCALE[p]} |")
    add("")

    # ---- 3. glossary ----
    add("## 3. Glossary")
    add("")
    if glossary:
        add("The following terms are used consistently throughout the requirements.")
        add("")
        add("| Term | Definition | Replaces |")
        add("|---|---|---|")
        for g in sorted(glossary, key=lambda g: g.term.lower()):
            add(f"| **{_md(g.term)}** | {_md(g.definition)} | "
                f"{_md(', '.join(g.synonyms_replaced)) or '-'} |")
    else:
        add("_No glossary was produced._")
    add("")

    # ---- 4. sources ----
    add("## 4. Source documents")
    add("")
    add("| ID | File | Type | Title / subject | Date |")
    add("|---|---|---|---|---|")
    for d in docs:
        add(f"| {d.doc_id} | `{d.path}` | {d.doc_type.value} | {_md(d.title)} | "
            f"{d.date or '-'} |")
    add("")

    # ---- 5-6. requirements ----
    sections = [(5, "Functional requirements", [ReqType.FUNCTIONAL]),
                (6, "Non-functional requirements and constraints",
                 [ReqType.NON_FUNCTIONAL, ReqType.CONSTRAINT])]
    for num, title, types in sections:
        add(f"## {num}. {title}")
        add("")
        group = [r for r in reqs if r.req_type in types]
        if not group:
            add("_None._")
            add("")
        categories = sorted({r.category for r in group}, key=str.lower)
        for k, cat in enumerate(categories, start=1):
            add(f"### {num}.{k} {cat}")
            add("")
            for r in (r for r in group if r.category == cat):
                add(f"#### {r.req_id} - {r.name}")
                add("")
                add(f"**Priority:** {r.priority.value} &nbsp;·&nbsp; "
                    f"**Type:** {r.req_type.value.replace('_', '-')} &nbsp;·&nbsp; "
                    f"**Sources:** {', '.join(r.sources) or '-'}")
                add("")
                add(r.description.strip())
                add("")
                add(f"*Priority rationale:* {r.priority_rationale.strip()}")
                add("")

    # ---- 7. traceability ----
    add("## 7. Traceability")
    add("")
    add("### 7.1 Requirement to sources")
    add("")
    add("| Requirement | Name | Priority | Source documents |")
    add("|---|---|---|---|")
    for r in reqs:
        srcs = ", ".join(f"{s} (`{doc_by_id[s].path}`)" for s in r.sources)
        add(f"| {r.req_id} | {_md(r.name)} | {r.priority.value} | {srcs or '-'} |")
    add("")
    add("### 7.2 Source to requirements")
    add("")
    add("| Document | Requirements derived | Blacklisted |")
    add("|---|---|---|")
    for d in docs:
        rs = [r.req_id for r in reqs if d.doc_id in r.sources]
        bs = [b.entry_id for b in blacklist if d.doc_id in b.sources]
        add(f"| {d.doc_id} `{d.path}` | {', '.join(rs) or '**none**'} | "
            f"{', '.join(bs) or '-'} |")
    add("")

    # ---- 8. blacklist ----
    add("## 8. Blacklist (discarded statements)")
    add("")
    if not blacklist:
        add("_No statements were discarded._")
        add("")
    for b in blacklist:
        add(f"#### {b.entry_id} - {b.name}")
        add("")
        line = (f"**Reason:** {b.reason.value.replace('_', ' ')} &nbsp;·&nbsp; "
                f"**Sources:** {', '.join(b.sources) or '-'}")
        if b.conflicts_with:
            line += f" &nbsp;·&nbsp; **Conflicts with:** {b.conflicts_with}"
        add(line)
        add("")
        add(f"*Statement:* {b.description.strip()}")
        add("")
        add(f"*Why discarded:* {b.explanation.strip()}")
        add("")

    # ---- 9. open issues ----
    open_issues = list(state.get("validation_issues", []))
    if final_review and not final_review.approved:
        open_issues += final_review.issues
    open_issues.sort(key=lambda i: i.severity != Severity.MAJOR)   # major first
    if open_issues:
        add("## 9. Open issues")
        add("")
        add("Issues still reported when the review loop ended:")
        add("")
        for iss in open_issues:
            aff = f" ({', '.join(iss.affected[:8])}{'...' if len(iss.affected) > 8 else ''})" \
                if iss.affected else ""
            add(f"- **{iss.issue_type.value}** ({iss.severity.value}){aff} "
                f"[{iss.origin}]: {iss.description}")
        add("")
    if final_review:
        add("## Review summary")
        add("")
        add(final_review.summary)
        add("")
    return "\n".join(L)


def renderer_node(state: GraphState) -> dict:
    out = Path(state.get("output_dir", "out")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    md_path = out / "requirements.md"
    json_path = out / "requirements.json"
    md_path.write_text(render_markdown(state), encoding="utf-8")
    payload = {
        "documents": [d.model_dump(exclude={"text", "chunks"}) for d in state["documents"]],
        "glossary": [g.model_dump() for g in state.get("glossary", [])],
        "requirements": [r.model_dump(mode="json") for r in state.get("requirements", [])],
        "blacklist": [b.model_dump(mode="json") for b in state.get("blacklist", [])],
        "candidates": [c.model_dump(mode="json") for c in state.get("candidates", [])],
        "review_history": [r.model_dump(mode="json") for r in state.get("review_history", [])],
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str),
                         encoding="utf-8")
    print(f"[renderer] wrote {md_path} and {json_path.name}")
    return {"output_files": [str(md_path), str(json_path)]}
