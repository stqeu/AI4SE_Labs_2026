"""LLM-invoking (agentic) nodes of the network (ANS1, ANS4).

* extractor_node    - gpt-5-mini   : one parallel branch per document
* planner_node      - gpt-5.6-luna : sorts all candidates into topics + glossary
* consolidator_node - gpt-5.6-luna : one parallel branch per topic: merge,
                                     resolve conflicts, prioritise, blacklist
* reviewer_node     - gpt-6-luna   : independent critic driving the loop
* reviser_node      - gpt-5.6-luna : targeted fixes of the reviewed issues
"""
from __future__ import annotations

import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

from config import SETTINGS
from llm_client import LLMError, call_json
from nodes.deterministic import (candidate_text, fallback_plan, repair_plan)
from prompts import (COMPLETENESS_REPAIR, CONSOLIDATOR_SYSTEM, CONSOLIDATOR_USER,
                     EXTRACTOR_SYSTEM, EXTRACTOR_USER, PLANNER_SYSTEM, PLANNER_USER,
                     REVISER_SYSTEM, REVISER_USER, REVIEWER_SYSTEM, REVIEWER_USER,
                     WRITING_RULES)
from schemas import (PRIORITY_SCALE, BatchResult, BlacklistEntry, CandidateRequirement,
                     ConsolidatedDiscard, ConsolidatedRequirement, ConsolidationResult,
                     ExtractionResult, Issue, IssueType, PatchResult, PlanResult,
                     Requirement, ReviewReport, Severity, SourceDocument, Topic)
from similarity import cluster, top_k_similar
from state import BatchInput, ExtractorInput, GraphState

# validator findings that can never be approved away
BLOCKING_VALIDATOR_ISSUES = {IssueType.UNACCOUNTED, IssueType.SCHEMA, IssueType.REUSED,
                             IssueType.TOO_BROAD, IssueType.BAD_BLACKLIST}


def _priority_scale_text() -> str:
    return "\n".join(f"   - {p.value}: {d}" for p, d in PRIORITY_SCALE.items())


def _writing_rules() -> str:
    return WRITING_RULES.format(priority_scale=_priority_scale_text())


_QUOTES = re.compile(r"[\"'“”‘’`«»]")


def _squash(text: str) -> str:
    """Lower-case, collapse whitespace, drop quote characters of any style."""
    return re.sub(r"\s+", " ", _QUOTES.sub("", text)).strip().lower()


# ==========================================================================
# 1. EXTRACTOR
# ==========================================================================
def extract_document(doc: SourceDocument) -> list[CandidateRequirement]:
    """Extract candidates from one document (all of its chunks)."""
    return extract_document_checked(doc)[0]


def extract_document_checked(doc: SourceDocument
                             ) -> tuple[list[CandidateRequirement], int]:
    """Like extract_document, but also returns the number of failed chunks."""
    found = []
    failed = 0
    n = len(doc.chunks)
    for k, chunk in enumerate(doc.chunks, start=1):
        note = (f"(This is part {k} of {n} of the document; parts overlap "
                f"slightly.)" if n > 1 else "")
        user = EXTRACTOR_USER.format(
            doc_id=doc.doc_id, path=doc.path, doc_type=doc.doc_type.value,
            title=doc.title, date=doc.date or "unknown",
            author=doc.author or "unknown", chunk_note=note, text=chunk)
        label = f"extract {doc.doc_id}" + (f" part {k}/{n}" if n > 1 else "")
        try:
            result = call_json(SETTINGS.model_extractor, EXTRACTOR_SYSTEM, user,
                               ExtractionResult, SETTINGS.max_tokens_extractor, label)
            found.extend(result.requirements)
        except Exception as exc:  # noqa: BLE001 - never kill the whole run
            failed += 1
            print(f"  [{label}] FAILED: {type(exc).__name__}: {str(exc)[:200]}")

    text = _squash(doc.text)
    cands = []
    for i, r in enumerate(found, start=1):
        cands.append(CandidateRequirement(
            **r.model_dump(), cand_id=f"{doc.doc_id}-C{i:02d}",
            source_doc_id=doc.doc_id,                       # [OS4] set by code
            evidence_found=_evidence_in(r.evidence, text)))
    return cands, failed


def _evidence_in(evidence: str, squashed_text: str) -> bool:
    """Deterministic check that the quote really occurs in the source.
    Quotes shortened with '...' are checked piece by piece."""
    parts = [p.strip() for p in re.split(r"\.\.\.|…", _squash(evidence))]
    parts = [p for p in parts if len(p) > 3]
    return bool(parts) and all(p in squashed_text for p in parts)


def _cache_path(cache_dir: str, doc: SourceDocument) -> Path:
    """Cache key changes whenever the model, prompt, schema or text changes."""
    key = hashlib.sha256("\x00".join([
        SETTINGS.model_extractor, EXTRACTOR_SYSTEM, EXTRACTOR_USER,
        json.dumps(ExtractionResult.model_json_schema()), doc.path, doc.text,
        str(SETTINGS.chunk_chars)]).encode("utf-8")).hexdigest()[:16]
    return Path(cache_dir) / f"{doc.doc_id}_{key}.json"


def extractor_node(payload: ExtractorInput) -> dict:
    doc = payload["document"]
    cache_dir = payload.get("cache_dir")
    cache = _cache_path(cache_dir, doc) if cache_dir else None
    if cache and cache.exists():
        cands = [CandidateRequirement.model_validate(c)
                 for c in json.loads(cache.read_text(encoding="utf-8"))]
        print(f"[extractor] {doc.doc_id} {doc.path}: {len(cands)} candidates (cached)\n",
              end="", flush=True)
        return {"candidates": cands}

    cands, failed = extract_document_checked(doc)
    verified = sum(bool(c.evidence_found) for c in cands)
    print(f"[extractor] {doc.doc_id} {doc.path}: {len(cands)} candidates "
          f"({verified} with verbatim evidence)"
          + (f" - WARNING: {failed} part(s) failed, result NOT cached" if failed else "")
          + "\n", end="", flush=True)
    # a partial extraction must never be cached, or re-runs would reuse the gap
    if cache and cands and not failed and not payload.get("cache_readonly"):
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps([c.model_dump(mode="json") for c in cands],
                                    ensure_ascii=False, indent=1), encoding="utf-8")
    return {"candidates": cands}


# ==========================================================================
# shared formatting helpers
# ==========================================================================
def _fmt_documents(docs: list[SourceDocument]) -> str:
    return "\n".join(f"{d.doc_id} | {d.doc_type.value} | {d.date or 'undated'} | "
                     f"{d.title} ({d.path})" for d in docs)


def _fmt_candidates(cands: list[CandidateRequirement], full: bool = True) -> str:
    lines = []
    for c in cands:
        if full:
            hint = f" [{c.stakeholder_priority_hint}]" if c.stakeholder_priority_hint else ""
            ev = c.evidence[:160].replace("\n", " ")
            lines.append(f"{c.cand_id} | {c.req_type.value} | {c.category} | "
                         f"{c.name} :: {c.description}{hint} {{{ev}}}")
        else:
            lines.append(f"{c.cand_id} | {c.name} :: {c.description}")
    return "\n".join(lines)


def _fmt_issues(issues: list[Issue]) -> str:
    if not issues:
        return "(none)"
    return "\n".join(
        f"- [{i.origin}, {i.severity.value}] {i.issue_type.value} {i.affected[:12]}"
        f"{'...' if len(i.affected) > 12 else ''}: {i.description}"
        + (f" -> fix: {i.suggested_fix}" if i.suggested_fix else "")
        for i in issues)


def _fmt_glossary(glossary) -> str:
    return "\n".join(f"- {g.term}: {g.definition} (replaces: "
                     f"{', '.join(g.synonyms_replaced) or '-'})"
                     for g in glossary) or "(none)"


def _docs_for(cands: list[CandidateRequirement],
              docs: list[SourceDocument]) -> list[SourceDocument]:
    used = {c.source_doc_id for c in cands}
    return [d for d in docs if d.doc_id in used]


def _accounted(result) -> set[str]:
    return ({i for r in result.requirements for i in r.merged_from}
            | {i for b in result.blacklist for i in b.candidate_ids})


def _restrict(result, allowed: set[str]):
    """Drop candidate IDs that do not belong to this call (no cross-talk)."""
    for r in result.requirements:
        r.merged_from = [i for i in dict.fromkeys(r.merged_from) if i in allowed]
    for b in result.blacklist:
        b.candidate_ids = [i for i in dict.fromkeys(b.candidate_ids) if i in allowed]
    return result


def call_complete(model: str, system: str, user: str, schema, ids: set[str],
                  max_tokens: int, label: str):
    """LLM call whose result must account for every ID in ``ids``.
    One follow-up repair call is made if some are missing (deterministic
    check), then foreign IDs are stripped."""
    result = call_json(model, system, user, schema, max_tokens, label)
    missing = ids - _accounted(result)
    if missing:
        print(f"  [{label}] {len(missing)} candidate(s) unaccounted -> repair call\n",
              end="", flush=True)
        history = [{"role": "assistant", "content": result.model_dump_json()},
                   {"role": "user", "content": COMPLETENESS_REPAIR.format(
                       missing=", ".join(sorted(missing)))}]
        try:
            fixed = call_json(model, system, user, schema, max_tokens,
                              f"{label} repair", history=history)
            if len(ids - _accounted(fixed)) < len(missing):
                result = fixed
        except Exception as exc:  # noqa: BLE001 - keep the first answer
            print(f"  [{label}] repair failed: {exc}")
    return _restrict(result, ids)


# ==========================================================================
# 2. PLANNER
# ==========================================================================
def planner_node(state: GraphState) -> dict:
    cands = state.get("candidates", [])
    n_topics = max(3, min(40, round(len(cands) / 30)))
    user = PLANNER_USER.format(
        n_candidates=len(cands),
        candidates="\n".join(f"{c.cand_id} | {c.req_type.value} | {c.category} | "
                             f"{c.name}" for c in cands))
    print(f"[planner] {len(cands)} candidates -> {SETTINGS.model_planner} "
          f"(target ~{n_topics} topics) ...")
    try:
        plan = call_json(SETTINGS.model_planner, PLANNER_SYSTEM.format(n_topics=n_topics),
                         user, PlanResult, SETTINGS.max_tokens_planner, "plan")
    except Exception as exc:  # noqa: BLE001 - deterministic fallback
        print(f"  [planner] FAILED ({exc}); falling back to extractor categories")
        plan = fallback_plan(cands)
    topics, stats = repair_plan(plan, cands)
    sizes = [len(t.candidate_ids) for t in topics]
    print(f"[planner] -> {len({t.name for t in topics})} topics in {len(topics)} batches "
          f"(sizes {min(sizes, default=0)}-{max(sizes, default=0)}), "
          f"{len(plan.glossary)} glossary terms; repair: {stats}")
    return {"topics": topics, "plan_glossary": plan.glossary}


# ==========================================================================
# 3. CONSOLIDATOR  (one parallel branch per topic batch)
# ==========================================================================
def consolidator_node(payload: BatchInput) -> dict:
    topic: Topic = payload["batch_topic"]
    cands = payload["batch_candidates"]
    ids = {c.cand_id for c in cands}
    groups = cluster([candidate_text(c) for c in cands], SETTINGS.dedup_threshold)
    user = CONSOLIDATOR_USER.format(
        topic_id=topic.topic_id, topic_name=topic.name, topic_scope=topic.scope,
        other_topics="\n".join(f"- {t}" for t in payload["batch_all_topics"]
                               if not t.startswith(f"{topic.name}:")) or "(none)",
        glossary=_fmt_glossary(payload["batch_glossary"]),
        documents=_fmt_documents(_docs_for(cands, payload["batch_documents"])),
        clusters="\n".join(", ".join(cands[i].cand_id for i in g) for g in groups)
                 or "(none)",
        n_candidates=len(cands), candidates=_fmt_candidates(cands))
    system = CONSOLIDATOR_SYSTEM.format(writing_rules=_writing_rules())
    label = f"consolidate {topic.topic_id}"
    try:
        result = call_complete(SETTINGS.model_consolidator, system, user,
                               ConsolidationResult, ids,
                               SETTINGS.max_tokens_consolidator, label)
    except Exception as exc:  # noqa: BLE001 - the loop will pick them up
        print(f"  [{label}] FAILED: {type(exc).__name__}: {str(exc)[:200]} "
              f"-> {len(ids)} candidates left for the revision loop")
        result = ConsolidationResult(glossary=[], requirements=[], blacklist=[])
    left = len(ids - _accounted(result))
    print(f"[consolidator] {topic.topic_id} {topic.name}: {len(cands)} candidates -> "
          f"{len(result.requirements)} requirements, {len(result.blacklist)} "
          f"blacklisted" + (f", {left} unaccounted" if left else "") + "\n",
          end="", flush=True)
    return {"batch_results": [BatchResult(topic_id=topic.topic_id,
                                          topic_name=topic.name, result=result)]}


# ==========================================================================
# 4. REVIEWER
# ==========================================================================
def reviewer_node(state: GraphState) -> dict:
    reqs = state.get("requirements", [])
    bl = state.get("blacklist", [])
    v_issues = state.get("validation_issues", [])
    rnd = state.get("round", 0) + 1
    if state.get("halt"):                    # revision impossible -> stop the loop
        prev = state.get("review")
        report = ReviewReport(approved=False, issues=prev.issues if prev else [],
                              summary=f"{state['halt']} The previous result and its "
                                      "open issues are kept.")
        return {"review": report, "review_history": [report], "round": rnd}

    by_id = {c.cand_id: c for c in state.get("candidates", [])}

    def merged(ids: list[str]) -> str:
        return "; ".join(f"{i} {by_id[i].name}" for i in ids if i in by_id)

    major_v = [i for i in v_issues if i.severity == Severity.MAJOR]
    minor_v = len(v_issues) - len(major_v)
    user = REVIEWER_USER.format(
        priority_scale=_priority_scale_text(),
        glossary=_fmt_glossary(state.get("glossary", [])),
        n_reqs=len(reqs),
        requirements="\n\n".join(
            f"{r.req_id} [{r.priority.value}, {r.req_type.value}, {r.category}] {r.name}\n"
            f"  {r.description}\n  merged: {merged(r.merged_from)}" for r in reqs),
        n_bl=len(bl),
        blacklist="\n".join(
            f"{b.entry_id} [{b.reason.value}] {b.name}: {b.description} -- WHY: "
            f"{b.explanation} (conflicts_with: {b.conflicts_with or '-'})\n"
            f"  candidates: {merged(b.candidate_ids)}" for b in bl) or "(none)",
        validator_issues=_fmt_issues(major_v)
        + (f"\n(+ {minor_v} minor wording findings not listed)" if minor_v else ""))
    print(f"[reviewer] round {rnd}: {SETTINGS.model_reviewer} on {len(reqs)} "
          f"requirements ...")
    try:
        report = call_json(SETTINGS.model_reviewer, REVIEWER_SYSTEM, user, ReviewReport,
                           SETTINGS.max_tokens_reviewer, f"review r{rnd}")
    except LLMError as exc:
        print(f"  [reviewer] FAILED: {exc}")
        report = ReviewReport(approved=False, issues=[], summary=f"Review failed: {exc}")
    for i in report.issues:
        i.origin = "reviewer"

    # deterministic approval rule: no major reviewer issue, no blocking finding
    major_r = [i for i in report.issues if i.severity == Severity.MAJOR]
    blocking = [i for i in v_issues if i.issue_type in BLOCKING_VALIDATOR_ISSUES
                and i.severity == Severity.MAJOR]
    approved = not major_r and not blocking
    if approved != report.approved:
        report.summary += (f" [Verdict set by rule: {len(major_r)} major reviewer "
                           f"issue(s), {len(blocking)} blocking validator finding(s).]")
    report.approved = approved
    print(f"[reviewer] -> {'APPROVED' if approved else 'changes requested'}: "
          f"{len(major_r)} major, {len(report.issues) - len(major_r)} minor issues, "
          f"{len(blocking)} blocking validator findings")
    return {"review": report, "review_history": [report], "round": rnd}


# ==========================================================================
# 5. REVISER  (targeted fixes, feedback loop)
# ==========================================================================
_REF = re.compile(r"\b(?:FR|NFR|CON|BL)-\d{3}\b|\bD\d+-C\d+\b|\bD\d{2,}\b")
_ITEM = re.compile(r"^(?:FR|NFR|CON|BL)-\d{3}$")


@dataclass
class Package:
    req_ids: set[str] = field(default_factory=set)
    bl_ids: set[str] = field(default_factory=set)
    loose: set[str] = field(default_factory=set)
    issues: list[Issue] = field(default_factory=list)

    def candidate_ids(self, reqs: dict, bls: dict) -> set[str]:
        ids = set(self.loose)
        for r in self.req_ids:
            ids |= set(reqs[r].merged_from)
        for b in self.bl_ids:
            ids |= set(bls[b].candidate_ids)
        return ids


def build_packages(issues: list[Issue], reqs: list[Requirement],
                   blacklist: list[BlacklistEntry],
                   candidates: list[CandidateRequirement],
                   max_candidates: int = SETTINGS.max_package_candidates,
                   max_items_per_issue: int = 12
                   ) -> tuple[list[Package], list[Issue], list[Issue]]:
    """Group issues into independent, size-capped work packages (deterministic).

    * items (requirements / blacklist entries) named by one issue must be
      revised together, so they go into the same package;
    * a loose (unaccounted) candidate joins the package of its most similar
      requirement, or gets a package of its own;
    * no package grows beyond ``max_candidates`` candidates - an issue that
      would require that is deferred to the next round (it stays open);
    * issues are packed major-first, so the important fixes happen first;
      minor (cosmetic) issues never open a package of their own - they are
      fixed only where a package exists anyway (saves calls).
    Returns (packages, unresolved issues, deferred issues).
    """
    req_by = {r.req_id: r for r in reqs}
    bl_by = {b.entry_id: b for b in blacklist}
    cand_by = {c.cand_id: c for c in candidates}
    owner: dict[str, list[str]] = {}
    for r in reqs:
        for i in r.merged_from:
            owner.setdefault(i, []).append(r.req_id)
    for b in blacklist:
        for i in b.candidate_ids:
            owner.setdefault(i, []).append(b.entry_id)

    def weight(item: str) -> int:
        if item.startswith("loose:"):
            return 1
        x = req_by.get(item) or bl_by.get(item)
        return len(x.merged_from if item in req_by else x.candidate_ids)

    packages: list[Package] = []
    pkg_of: dict[str, int] = {}
    sizes: list[int] = []

    def place(items: list[str], iss: Issue | None) -> bool:
        """Put items (and the issue) into one package if the cap allows."""
        existing = sorted({pkg_of[x] for x in items if x in pkg_of})
        fresh = [x for x in dict.fromkeys(items) if x not in pkg_of]
        total = sum(sizes[k] for k in existing) + sum(weight(x) for x in fresh)
        if existing and total > max_candidates:
            return False
        if existing:
            k = existing[0]
            for other in existing[1:]:                # merge packages
                o = packages[other]
                packages[k].req_ids |= o.req_ids
                packages[k].bl_ids |= o.bl_ids
                packages[k].loose |= o.loose
                packages[k].issues += [i for i in o.issues if i not in packages[k].issues]
                for x in list(pkg_of):
                    if pkg_of[x] == other:
                        pkg_of[x] = k
                sizes[k] += sizes[other]
                packages[other], sizes[other] = Package(), 0
        else:
            packages.append(Package())
            sizes.append(0)
            k = len(packages) - 1
        for x in fresh:
            pkg_of[x] = k
            sizes[k] += weight(x)
            if x.startswith("loose:"):
                packages[k].loose.add(x[6:])
            elif x in req_by:
                packages[k].req_ids.add(x)
            else:
                packages[k].bl_ids.add(x)
        if iss is not None and iss not in packages[k].issues:
            packages[k].issues.append(iss)
        return True

    unresolved: list[Issue] = []
    deferred: list[Issue] = []
    loose_all: list[str] = []
    ordered = sorted(issues, key=lambda i: (i.severity != Severity.MAJOR,
                                            i.origin != "reviewer"))
    for iss in ordered:
        refs = list(dict.fromkeys(iss.affected + _REF.findall(
            f"{iss.description} {iss.suggested_fix or ''}")))
        items: list[str] = []
        for ref in refs:
            if ref in req_by or ref in bl_by:
                items.append(ref)
            elif ref in cand_by:
                if ref in owner:
                    items += owner[ref]
                elif ref not in loose_all:
                    loose_all.append(ref)
            elif iss.issue_type == IssueType.MISSING and re.fullmatch(r"D\d+", ref):
                items += [b.entry_id for b in blacklist if ref in b.sources][:5]
        items = list(dict.fromkeys(items))
        if not items and not any(r in cand_by and r not in owner for r in refs):
            unresolved.append(iss)
            continue
        if iss.issue_type == IssueType.UNACCOUNTED and not items:
            continue                      # loose candidates are placed below
        if iss.severity == Severity.MINOR and not any(x in pkg_of for x in items):
            deferred.append(iss)          # cosmetic: only piggy-backs on packages
            continue                      # that are revised for a major issue
        # chunk a very wide issue by count and by candidate weight
        chunks: list[list[str]] = [[]]
        for x in items:
            if chunks[-1] and (len(chunks[-1]) >= max_items_per_issue or
                               sum(map(weight, chunks[-1])) + weight(x) > max_candidates):
                chunks.append([])
            chunks[-1].append(x)
        placed = [place(ch, iss) for ch in chunks if ch]
        if not all(placed):
            deferred.append(iss)

    # loose candidates: join the package of the most similar requirement
    if loose_all:
        hits = top_k_similar([candidate_text(cand_by[c]) for c in loose_all],
                             [f"{r.name}. {r.name}. {r.description}" for r in reqs], 1) \
            if reqs else [[] for _ in loose_all]
        for cid, hit in zip(loose_all, hits):
            near = [reqs[j].req_id for j, score in hit if score >= 0.2]
            if not (near and place(near + [f"loose:{cid}"], None)):
                place([f"loose:{cid}"], None)

    # bin-pack small packages together (largest first, first fit)
    live = [(packages[k], sizes[k]) for k in range(len(packages))
            if packages[k].req_ids or packages[k].bl_ids or packages[k].loose]
    bins: list[list] = []
    for pkg, size in sorted(live, key=lambda x: -x[1]):
        for b in bins:
            if b[1] + size <= max_candidates:
                b[0].req_ids |= pkg.req_ids
                b[0].bl_ids |= pkg.bl_ids
                b[0].loose |= pkg.loose
                b[0].issues += [i for i in pkg.issues if i not in b[0].issues]
                b[1] += size
                break
        else:
            bins.append([pkg, size])
    return [b[0] for b in bins], unresolved, deferred


def _strip_id_prefix(conflicts_with: str | None) -> str | None:
    """'FR-003 (Name)' -> 'Name' (IDs are renumbered every round)."""
    if not conflicts_with:
        return conflicts_with
    m = re.match(r"^(?:FR|NFR|CON)-\d{3} \((.*)\)$", conflicts_with)
    return m.group(1) if m else conflicts_with


def _to_consolidated(r: Requirement) -> ConsolidatedRequirement:
    return ConsolidatedRequirement(**r.model_dump(exclude={"req_id", "sources"}))


def _to_discard(b: BlacklistEntry) -> ConsolidatedDiscard:
    d = ConsolidatedDiscard(**b.model_dump(exclude={"entry_id", "sources"}))
    d.conflicts_with = _strip_id_prefix(d.conflicts_with)
    return d


def _snap_category(cat: str, topic_names: list[str]) -> str:
    for t in topic_names:
        if t.lower() == cat.strip().lower():
            return t
    hit = top_k_similar([cat], topic_names, 1)[0] if topic_names else []
    return topic_names[hit[0][0]] if hit and hit[0][1] > 0 else cat


def revise_package(pkg: Package, state: GraphState, label: str) -> PatchResult:
    req_by = {r.req_id: r for r in state.get("requirements", [])}
    bl_by = {b.entry_id: b for b in state.get("blacklist", [])}
    cand_by = {c.cand_id: c for c in state.get("candidates", [])}
    ids = pkg.candidate_ids(req_by, bl_by)
    cands = [cand_by[i] for i in sorted(ids) if i in cand_by]
    issues_text = _fmt_issues(pkg.issues) if pkg.issues else ""
    if pkg.loose:
        issues_text += (f"\n- [validator, major] unaccounted_candidate: these candidates "
                        f"are not yet in any requirement or blacklist entry: "
                        f"{', '.join(sorted(pkg.loose))}. Merge each into the matching "
                        "requirement, create a new requirement, or blacklist it.")
    topics = []
    for t in state.get("topics", []):
        line = f"- {t.name}: {t.scope}"
        if line not in topics:
            topics.append(line)
    user = REVISER_USER.format(
        topics="\n".join(topics), glossary=_fmt_glossary(state.get("glossary", [])),
        documents=_fmt_documents(_docs_for(cands, state["documents"])),
        issues=issues_text.strip() or "(none)",
        requirements="\n\n".join(
            f"{r.req_id} [{r.priority.value}, {r.req_type.value}, {r.category}] {r.name}\n"
            f"  {r.description}\n  priority_rationale: {r.priority_rationale}\n"
            f"  merged_from: {', '.join(r.merged_from)}"
            for r in (req_by[i] for i in sorted(pkg.req_ids))) or "(none)",
        blacklist="\n".join(
            f"{b.entry_id} [{b.reason.value}] {b.name}: {b.description} -- WHY: "
            f"{b.explanation} (conflicts_with: {_strip_id_prefix(b.conflicts_with) or '-'}"
            f"; candidate_ids: {', '.join(b.candidate_ids)})"
            for b in (bl_by[i] for i in sorted(pkg.bl_ids))) or "(none)",
        n_candidates=len(cands), candidates=_fmt_candidates(cands))
    system = REVISER_SYSTEM.format(writing_rules=_writing_rules())
    return call_complete(SETTINGS.model_consolidator, system, user, PatchResult, ids,
                         SETTINGS.max_tokens_consolidator, label)


def reviser_node(state: GraphState) -> dict:
    reqs = state.get("requirements", [])
    bl = state.get("blacklist", [])
    review = state.get("review")
    issues = list(state.get("validation_issues", [])) + (review.issues if review else [])
    packages, unresolved, deferred = build_packages(issues, reqs, bl,
                                                    state.get("candidates", []))
    rnd = state.get("round", 0)
    print(f"[reviser] round {rnd}: {len(issues)} issues -> {len(packages)} work "
          f"packages; {len(deferred)} deferred (size cap / minor), {len(unresolved)} "
          f"reference nothing actionable")
    if not packages:
        return {"halt": "No actionable issues left for revision."}

    def run(k_pkg):
        k, pkg = k_pkg
        try:
            return pkg, revise_package(pkg, state, f"revise r{rnd} p{k}")
        except Exception as exc:  # noqa: BLE001 - keep the old items
            print(f"  [revise r{rnd} p{k}] FAILED: {type(exc).__name__}: {str(exc)[:200]}")
            return pkg, None

    with ThreadPoolExecutor(max_workers=SETTINGS.revise_concurrency) as ex:
        results = list(ex.map(run, enumerate(packages, start=1)))
    if all(patch is None for _, patch in results):
        return {"halt": f"All {len(packages)} revision packages failed in round {rnd}."}

    topic_names = list(dict.fromkeys(t.name for t in state.get("topics", [])))
    replaced_r: set[str] = set()
    replaced_b: set[str] = set()
    new_r: list[ConsolidatedRequirement] = []
    new_b: list[ConsolidatedDiscard] = []
    for pkg, patch in results:
        if patch is None:
            continue
        replaced_r |= pkg.req_ids
        replaced_b |= pkg.bl_ids
        for r in patch.requirements:
            r.category = _snap_category(r.category, topic_names)
            new_r.append(r)
        for d in patch.blacklist:
            d.conflicts_with = _strip_id_prefix(d.conflicts_with)
            new_b.append(d)
    consolidation = ConsolidationResult(
        glossary=state.get("glossary", []),
        requirements=[_to_consolidated(r) for r in reqs if r.req_id not in replaced_r]
        + new_r,
        blacklist=[_to_discard(b) for b in bl if b.entry_id not in replaced_b] + new_b)
    print(f"[reviser] replaced {len(replaced_r)} requirements / {len(replaced_b)} "
          f"blacklist entries with {len(new_r)} / {len(new_b)}")
    return {"consolidation": consolidation}
