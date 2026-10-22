"""Fake LLM for ``main.py --mock``: tests the whole graph with NO API calls.

Replaces ``llm_client._raw_call`` with canned, prompt-aware answers. It is
deliberately imperfect so that every safety net is exercised:
* extractor    - 2-3 candidates per chunk (only used for documents that are
                 not in the extraction cache)
* planner      - topics = extractor categories, but forgets ~5% of the
                 candidates and invents one ID (-> plan repair)
* consolidator - merges candidates with identical names, blacklists one
                 statement in larger topics, and forgets one candidate in the
                 first answer of every batch (-> completeness repair call)
* reviewer     - round 1: one major duplicate issue + one minor issue;
                 later rounds: no issues (-> approval by rule)
* reviser      - merges the requirements named in a duplicate issue and turns
                 loose candidates into requirements
The text is meaningless; only the plumbing is being tested.
"""
from __future__ import annotations

import json
import re

import llm_client

_state = {"reviews": 0}
_LONG = (" It was requested by stakeholders in the source documents and supports "
         "their daily work. Staff in every Branch use it. It is verifiable by a "
         "test in the staff client. (mock text)")
_CAND = re.compile(r"^(D\d+-C\d+) \| (\w+) \| ([^|]+) \| (.+?) ::", re.M)


def _req(name: str, rtype: str, cat: str, ids: list[str], prio: str = "Should") -> dict:
    return {"name": name[:60], "description": f"The system shall provide {name.lower()}."
            + _LONG, "req_type": rtype, "category": cat, "priority": prio,
            "priority_rationale": "Mock rationale.", "merged_from": ids}


def _extract(user: str) -> dict:
    doc_id = re.search(r"^Document (D\d+):", user, re.M).group(1)
    words = user.split("----- DOCUMENT TEXT -----", 1)[1].split()
    quote = " ".join(words[5:12]) if len(words) > 12 else " ".join(words)
    return {"requirements": [
        {"name": f"Mock Report For {doc_id}", "description": "A report.",
         "req_type": "functional", "category": "Reporting", "evidence": quote},
        {"name": f"Mock Quality For {doc_id}", "description": "Fast.",
         "req_type": "non_functional", "category": "Performance", "evidence": quote}]}


def _plan(user: str) -> dict:
    rows = re.findall(r"^(D\d+-C\d+) \| (\w+) \| ([^|\n]+) \| ", user, re.M)
    topics: dict[str, list[str]] = {}
    for k, (cid, _, cat, ) in enumerate(rows):
        if k % 20 == 7:                      # forget ~5%
            continue
        topics.setdefault(cat.strip().title(), []).append(cid)
    out = [{"name": n, "scope": f"Everything about {n.lower()}.", "candidate_ids": ids}
           for n, ids in topics.items()]
    if out:
        out[0]["candidate_ids"].append("D99-C99")   # invented ID
    return {"glossary": [{"term": "Patron", "definition": "Library user.",
                          "synonyms_replaced": ["borrower", "customer"]},
                         {"term": "Branch", "definition": "A library location.",
                          "synonyms_replaced": ["location"]}],
            "topics": out}


def _consolidate(user: str, is_repair: bool) -> dict:
    topic = re.search(r"^TOPIC \S+: (.+)$", user, re.M).group(1)
    rows = _CAND.findall(user)
    groups: dict[str, list] = {}
    for cid, rtype, _, name in rows:
        groups.setdefault(name.strip().lower(), []).append((cid, rtype, name.strip()))
    keys = list(groups)
    discard = keys.pop() if len(keys) >= 6 else None
    reqs = [_req(groups[k][0][2], groups[k][0][1], topic, [c for c, _, _ in groups[k]],
                 ["Must", "Should", "Could"][i % 3]) for i, k in enumerate(keys)]
    if not is_repair and reqs and reqs[-1]["merged_from"]:
        reqs[-1]["merged_from"] = reqs[-1]["merged_from"][:-1] or reqs[-1]["merged_from"]
        if len(reqs) > 1:
            reqs.pop()                       # forget a candidate -> repair call
    bl = [] if not discard else [{
        "name": groups[discard][0][2], "description": "Mock discarded statement.",
        "reason": "nonsensical", "explanation": "Discarded by the mock to exercise "
        "the blacklist section of the document.", "conflicts_with": None,
        "candidate_ids": [c for c, _, _ in groups[discard]]}]
    return {"glossary": [], "requirements": reqs, "blacklist": bl}


def _review(user: str) -> dict:
    _state["reviews"] += 1
    ids = re.findall(r"^((?:FR|NFR|CON)-\d{3}) \[", user, re.M)
    if _state["reviews"] == 1 and len(ids) >= 2:
        return {"approved": False, "summary": "Mock review: please revise.", "issues": [
            {"issue_type": "duplicate", "severity": "major", "affected": ids[:2],
             "description": f"{ids[0]} and {ids[1]} describe the same need.",
             "suggested_fix": "Merge them."},
            {"issue_type": "weak_description", "severity": "minor",
             "affected": [ids[2 % len(ids)]], "description": "Mock wording issue.",
             "suggested_fix": "Reword."}]}
    return {"approved": True, "issues": [], "summary": "Mock review: approved."}


def _revise(user: str) -> dict:
    blocks = re.findall(r"^((?:FR|NFR|CON)-\d{3}) \[(\w+), (\w+), ([^\]]+)\] (.+)\n"
                        r"(?:.*\n){2}  merged_from: (.*)$", user, re.M)
    dup = re.findall(r"duplicate \[([^\]]*)\]", user)
    dup_ids = set(re.findall(r"(?:FR|NFR|CON)-\d{3}", " ".join(dup)))
    reqs, merged_dup = [], None
    for rid, prio, rtype, cat, name, merged in blocks:
        ids = [i.strip() for i in merged.split(",") if i.strip()]
        if rid in dup_ids:
            if merged_dup is None:
                merged_dup = _req(name, rtype, cat, ids, prio)
                reqs.append(merged_dup)
            else:
                merged_dup["merged_from"] += ids
            continue
        reqs.append(_req(name, rtype, cat, ids, prio))
    bl = []
    for reason, name, ids in re.findall(
            r"^BL-\d{3} \[(\w+)\] ([^:]+):.*candidate_ids: ([^)]*)\)$", user, re.M):
        bl.append({"name": name, "description": "Mock discarded statement.",
                   "reason": reason, "explanation": "Kept as discarded by the mock "
                   "reviser in this revision round.", "conflicts_with": None,
                   "candidate_ids": [i.strip() for i in ids.split(",")]})
    loose = re.search(r"not yet in any requirement or blacklist entry: ([^.]+)\.", user)
    cat = re.search(r"^- ([^:]+):", user, re.M).group(1)
    if loose:
        for cid in loose.group(1).split(", "):
            reqs.append(_req(f"Recovered Need {cid}", "functional", cat, [cid.strip()]))
    return {"requirements": reqs, "blacklist": bl}


def _fake_raw_call(model: str, messages: list[dict], max_tokens: int):
    system, user = messages[0]["content"], messages[1]["content"]
    if "senior requirements engineer" in system:
        out = _extract(user)
    elif "preparing consolidation" in system:
        out = _plan(user)
    elif "candidate\nrequirements of ONE topic" in system:
        out = _consolidate(user, is_repair=len(messages) > 2)
    elif "revising a requirements set" in system:
        out = _revise(user)
    elif "requirements quality reviewer" in system:
        out = _review(user)
    else:
        raise RuntimeError("mock: unknown prompt")
    text = json.dumps(out)
    llm_client.USAGE.add(f"{model} (mock)", sum(len(m["content"]) for m in messages) // 4,
                         len(text) // 4, 0.0)
    return text, "stop"


def install() -> None:
    llm_client._raw_call = _fake_raw_call
    print("*** MOCK MODE: no API calls will be made ***")
