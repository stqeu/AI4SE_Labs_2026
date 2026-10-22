"""Run ONLY the Extractor on selected documents - to check quality and cost
before running the whole network.

Usage:
    python try_extractor.py                 # list documents, no API call
    python try_extractor.py --doc D13       # extract one document (1 call)
    python try_extractor.py --doc D13 --doc conv_pines018
    python try_extractor.py --all           # every document (~22 calls)

Results are saved to out_test/candidates_<ids>.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import SETTINGS
from llm_client import USAGE
from nodes.deterministic import load_documents
from nodes.llm import extract_document

HERE = Path(__file__).resolve().parent


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default=str(HERE.parent / "data" / "corpus"))
    ap.add_argument("--doc", action="append", default=[],
                    help="document ID (D13) or part of its file name; repeatable")
    ap.add_argument("--all", action="store_true", help="extract every document")
    ap.add_argument("--output", default=str(HERE / "out_test"))
    args = ap.parse_args()

    docs = load_documents(args.input)
    if args.all:
        selected = docs
    else:
        selected = [d for d in docs if any(
            s.lower() == d.doc_id.lower() or s.lower() in d.path.lower()
            for s in args.doc)]
    if not selected:
        print("Documents (pass --doc <ID> to extract one; no API call was made):")
        for d in docs:
            print(f"  {d.doc_id}  {d.doc_type.value:<16} {len(d.chunks)} chunk(s)  {d.path}")
        return

    print(f"Extractor model: {SETTINGS.model_extractor}\n")
    all_cands = []
    for d in selected:
        cands = extract_document(d)
        all_cands += cands
        print(f"\n=== {d.doc_id} {d.path}: {len(cands)} candidates ===")
        for c in cands:
            ok = "ok " if c.evidence_found else "?? "
            hint = f"  [{c.stakeholder_priority_hint}]" if c.stakeholder_priority_hint else ""
            print(f"{c.cand_id} {c.req_type.value[:7]:<7} {c.category[:18]:<18} "
                  f"{c.name}{hint}")
            print(f"        {c.description}")
            print(f"        {ok}\"{c.evidence[:110]}\"")

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    tag = "all" if args.all else "_".join(d.doc_id for d in selected)
    path = out / f"candidates_{tag}.json"
    path.write_text(json.dumps([c.model_dump(mode="json") for c in all_cands],
                               indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved {len(all_cands)} candidates to {path}")
    print("'ok' = evidence quote found verbatim in the source, '??' = not found\n")
    print(USAGE.report())


if __name__ == "__main__":
    main()
