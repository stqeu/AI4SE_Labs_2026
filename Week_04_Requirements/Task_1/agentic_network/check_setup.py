"""Step 1 sanity check: dependencies, API key, model access, input corpus.

Usage:
    python check_setup.py [--input ../data/corpus] [--all-models]
"""
from __future__ import annotations

import argparse
import importlib
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALL_MODELS = [
    "gpt-6-luna", "gpt-5.6-luna", "gpt-5.4-nano", "gpt-5-nano",
    "gpt-5-mini", "gpt-4.1-nano", "gpt-4o-mini",
]
REQUIRED_PACKAGES = ["langgraph", "langchain_openai", "langchain_core",
                     "openai", "pydantic", "dotenv"]
TEXT_SUFFIXES = {".txt", ".md", ".eml"}


def ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def check_packages() -> bool:
    print("1) Python packages")
    good = True
    for name in REQUIRED_PACKAGES:
        try:
            mod = importlib.import_module(name)
            ok(f"{name} {getattr(mod, '__version__', '')}".rstrip())
        except ImportError as exc:
            fail(f"{name}: {exc}")
            good = False
    return good


def check_key() -> bool:
    print("2) API key")
    try:
        from dotenv import load_dotenv
        load_dotenv(HERE / ".env")
    except ImportError:
        fail("python-dotenv not installed - run setup.ps1 first")
        return False
    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key.startswith("sk-..."):
        fail("OPENAI_API_KEY missing - set it in .env")
        return False
    ok(f"OPENAI_API_KEY found (…{key[-4:]})")
    return True


def check_models(models: list[str]) -> bool:
    print("3) Model access (one tiny request each)")
    from openai import OpenAI
    client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL") or None)
    good = True
    for model in models:
        t0 = time.time()
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Reply with the single word: pong"}],
                max_completion_tokens=200,  # reasoning models need headroom
            )
            text = (resp.choices[0].message.content or "").strip()
            ok(f"{model:<14} {time.time() - t0:5.1f}s  -> {text[:30]!r}")
        except Exception as exc:  # noqa: BLE001 - report any API error
            fail(f"{model:<14} {type(exc).__name__}: {str(exc)[:120]}")
            good = False
    return good


def check_corpus(input_dir: Path) -> bool:
    print(f"4) Input corpus: {input_dir}")
    if not input_dir.is_dir():
        fail("directory not found")
        return False
    files = sorted(p for p in input_dir.rglob("*")
                   if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES)
    if not files:
        fail("no .txt/.md/.eml files found")
        return False
    total = sum(p.stat().st_size for p in files)
    ok(f"{len(files)} documents, {total / 1024:.0f} KB total")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=HERE.parent / "data" / "corpus",
                    help="input corpus directory")
    ap.add_argument("--all-models", action="store_true",
                    help="probe all 7 course models, not just the 3 configured ones")
    args = ap.parse_args()

    results = [check_packages()]
    key_ok = check_key()
    results.append(key_ok)
    if key_ok:
        configured = [os.getenv(v) for v in
                      ("MODEL_EXTRACTOR", "MODEL_CONSOLIDATOR", "MODEL_REVIEWER")]
        models = ALL_MODELS if args.all_models else [m for m in configured if m]
        if len(set(models)) < 3:
            fail("need 3 different models configured (ANS4)")
            results.append(False)
        results.append(check_models(models))
    results.append(check_corpus(args.input.resolve()))

    print("\nAll checks passed." if all(results) else "\nSome checks failed - see above.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
