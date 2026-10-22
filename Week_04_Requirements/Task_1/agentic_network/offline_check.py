"""Offline test of the deterministic nodes - makes NO API calls.

Runs loader -> (fake extractor) -> prededup -> (fake consolidator) ->
validator -> renderer on the real corpus, using hand-written stand-ins for
the LLM outputs. The fake consolidation contains deliberate mistakes so we
can see the validator report them.

Usage:
    python offline_check.py [--input ../data/corpus] [--output out_offline]
"""
from __future__ import annotations

import argparse
from pathlib import Path

from nodes.deterministic import (loader_node, prededup_node, renderer_node,
                                 validator_node)
from schemas import (CandidateRequirement, ConsolidatedDiscard,
                     ConsolidatedRequirement, ConsolidationResult,
                     DiscardReason, GlossaryTerm, Priority, ReqType)

HERE = Path(__file__).resolve().parent


def fake_candidates(docs) -> list[CandidateRequirement]:
    """Two generic candidates per document plus a few planted duplicates."""
    out = []
    for d in docs:
        base = [
            ("Report on " + d.title[:40], f"Users described in {d.path} need a report "
             "about circulation statistics per branch.", ReqType.FUNCTIONAL, "Reporting"),
            ("Fast response time", "Searches should return in under two seconds.",
             ReqType.NON_FUNCTIONAL, "Performance"),
        ]
        for k, (name, desc, rt, cat) in enumerate(base, start=1):
            out.append(CandidateRequirement(
                cand_id=f"{d.doc_id}-C{k:02d}", source_doc_id=d.doc_id, name=name,
                description=desc, req_type=rt, category=cat,
                evidence=d.text[:60].replace("\n", " ")))
    # planted duplicates in two different documents
    for d in (docs[0], docs[-1]):
        out.append(CandidateRequirement(
            cand_id=f"{d.doc_id}-C99", source_doc_id=d.doc_id,
            name="Staff card swipe login",
            description="Staff log in by swiping their employee ID card, with "
                        "username and password as a fallback.",
            req_type=ReqType.FUNCTIONAL, category="Security", evidence="swipe"))
    return out


def fake_consolidation(cands) -> ConsolidationResult:
    perf = [c.cand_id for c in cands if c.name == "Fast response time"]
    login = [c.cand_id for c in cands if c.name == "Staff card swipe login"]
    reports = [c.cand_id for c in cands if c.name.startswith("Report on")]
    long_desc = ("The system shall {x}. This was requested by several libraries "
                 "in interviews, meetings and email threads. It supports daily "
                 "staff work and reduces manual effort. Acceptance: the behaviour "
                 "is available to authorised staff in every branch.")
    return ConsolidationResult(
        glossary=[GlossaryTerm(term="Staff member", definition="Library employee "
                               "using the staff client.", synonyms_replaced=["employee", "librarian"])],
        requirements=[
            ConsolidatedRequirement(
                name="Branch circulation report",
                description=long_desc.format(x="produce circulation statistics per branch"),
                req_type=ReqType.FUNCTIONAL, category="reporting", priority=Priority.MUST,
                priority_rationale="Requested in most documents.",
                merged_from=reports[:-3]),          # MISTAKE: 3 left unaccounted
            ConsolidatedRequirement(
                name="Streamlined staff login",
                description=long_desc.format(x="let staff log in by card swipe or password"),
                req_type=ReqType.FUNCTIONAL, category="Security", priority=Priority.SHOULD,
                priority_rationale="Security and speed benefit.", merged_from=login),
            ConsolidatedRequirement(
                name="Search response time",
                description="Searches return fast.",   # MISTAKE: too short, wrong phrasing
                req_type=ReqType.NON_FUNCTIONAL, category="Performance",
                priority=Priority.SHOULD, priority_rationale="Usability.",
                merged_from=perf[1:] + ["D99-C01"]),  # MISTAKE: unknown ID
        ],
        blacklist=[ConsolidatedDiscard(
            name="Instant search", description="Search results in zero seconds.",
            reason=DiscardReason.NONSENSICAL,
            explanation="Zero latency is physically impossible; replaced by a "
                        "measurable response-time requirement.",
            conflicts_with="Search response time", candidate_ids=perf[:1])],
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(HERE.parent / "data" / "corpus"))
    ap.add_argument("--output", default=str(HERE / "out_offline"))
    args = ap.parse_args()

    state: dict = {"input_dir": args.input, "output_dir": args.output}
    state.update(loader_node(state))
    for d in state["documents"]:
        print(f"   {d.doc_id} {d.doc_type.value:<16} {len(d.text):>6} chars "
              f"{len(d.chunks)} chunk(s)  {d.path}  | {d.title[:50]}")

    state["candidates"] = fake_candidates(state["documents"])
    state.update(prededup_node(state))
    for g in state["clusters"][:5]:
        print("   group:", g[:8], "..." if len(g) > 8 else "")

    state["consolidation"] = fake_consolidation(state["candidates"])
    state.update(validator_node(state))
    for iss in state["validation_issues"]:
        print(f"   - {iss.issue_type.value}: {iss.description[:110]}")

    state["review_history"] = []
    state.update(renderer_node(state))


if __name__ == "__main__":
    main()
