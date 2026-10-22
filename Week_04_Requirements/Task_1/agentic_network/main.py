"""Requirements-refinement agentic network - command-line entry point.

Usage:
    python main.py --input ../data/corpus --mock          # free wiring test
    python main.py --input ../data/corpus                 # real run (asks first)
    python main.py --input ../data/corpus --output out --max-rounds 3 --yes

Outputs (in --output): requirements.md, requirements.json, graph.mmd,
cache/ (per-document extraction results, reused on re-runs).
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from config import SETTINGS
from llm_client import USAGE


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="directory with the input corpus")
    ap.add_argument("--output", default=None,
                    help="output directory (default: out, or out_mock with --mock)")
    ap.add_argument("--max-rounds", type=int, default=SETTINGS.max_rounds,
                    help="maximum consolidate/review rounds (feedback loop)")
    ap.add_argument("--concurrency", type=int, default=6,
                    help="max parallel extractor calls")
    ap.add_argument("--mock", action="store_true", help="fake LLM, no API calls")
    ap.add_argument("--no-cache", action="store_true", help="ignore extraction cache")
    ap.add_argument("--cache-dir", default=None,
                    help="extraction cache (default: <output>/cache; with --mock "
                         "the real out/cache is read, never written)")
    ap.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    args = ap.parse_args()

    out = Path(args.output or ("out_mock" if args.mock else "out")).resolve()
    # real runs read+write <output>/cache; mock runs only READ the real cache
    # (so they test consolidation on real candidates) and never write to it
    if args.no_cache:
        cache_dir = None
    elif args.mock:
        cache_dir = Path(args.cache_dir or "out/cache").resolve()
    else:
        cache_dir = Path(args.cache_dir).resolve() if args.cache_dir else out / "cache"

    # --- preview & confirmation (cheap, deterministic) ---------------------
    from nodes.deterministic import load_documents
    from nodes.llm import _cache_path
    docs = load_documents(args.input)
    if not docs:
        print(f"No input documents found in {args.input}")
        return 1
    cached = sum(1 for d in docs if cache_dir and _cache_path(str(cache_dir), d).exists())
    extract_calls = sum(len(d.chunks) for d in docs
                        if not (cache_dir and _cache_path(str(cache_dir), d).exists()))
    print(f"Input:  {Path(args.input).resolve()}  ({len(docs)} documents, "
          f"{cached} cached)")
    print(f"Output: {out}")
    print(f"Models: extractor={SETTINGS.model_extractor}  planner="
          f"{SETTINGS.model_planner}  consolidator/reviser="
          f"{SETTINGS.model_consolidator}  reviewer={SETTINGS.model_reviewer}")
    print(f"Planned LLM calls: {extract_calls} extraction, 1 planning, about one "
          f"consolidation per topic (+repairs), up to {args.max_rounds} reviews and "
          f"{args.max_rounds - 1} revision rounds of several small packages each")

    if args.mock:
        import mock_llm
        mock_llm.install()
    else:
        if not os.getenv("OPENAI_API_KEY"):
            print("OPENAI_API_KEY is not set (put it in .env).")
            return 1
        if not args.yes:
            if input("Proceed with real API calls? [y/N] ").strip().lower() != "y":
                print("Aborted - no API calls made.")
                return 0

    # --- run the graph -------------------------------------------------------
    from graph import build_graph
    app = build_graph()
    out.mkdir(parents=True, exist_ok=True)
    try:
        (out / "graph.mmd").write_text(app.get_graph().draw_mermaid(), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - diagram is optional
        print(f"(could not export graph diagram: {exc})")

    t0 = time.time()
    final = app.invoke(
        {"input_dir": str(Path(args.input).resolve()), "output_dir": str(out),
         "max_rounds": args.max_rounds,
         "cache_dir": str(cache_dir) if cache_dir else None,
         "cache_readonly": args.mock},
        config={"max_concurrency": args.concurrency, "recursion_limit": 100})

    review = final.get("review")
    print(f"\nDone in {time.time() - t0:.0f}s - {len(final.get('requirements', []))} "
          f"requirements, {len(final.get('blacklist', []))} blacklisted, "
          f"{final.get('round', 0)} review round(s), final verdict: "
          f"{'approved' if review and review.approved else 'not approved'}")
    for f in final.get("output_files", []):
        print(f"  -> {f}")
    print("\n" + USAGE.report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
