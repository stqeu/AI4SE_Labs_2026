"""RAG pipeline that implements missing methods with an LLM (Week 06, Task 5).

For every task in ``Assignments/missing_code.json``:
  1. take the textual task (location + docstring),
  2. retrieve the top-5 chunks for it (Task 4 retriever, Task 3 embeddings),
  3. send a prompt with the task + the 5 chunks to an LLM (gpt-5-mini),
  4. write the returned method into the target source file (replacing the stub).

Safety / cost controls (the API key is only used in step 3):
  --dry-run       build and save all prompts to prompts/, call NO API, change NO file
  --only X.y      process one task only (e.g. OrderStateMachine.transition)
  responses/      every LLM answer is cached; re-runs reuse it instead of calling
                  the API again (use --force to call again)
  no automatic re-asking: if the answer is not valid Python, the stub is kept
                  and the task is reported as failed
  --run-tests     run the unit tests afterwards (no API) -> test_results.txt
  --tests-only    only run the unit tests

Usage:
    python solver.py --dry-run
    python solver.py --only OrderStateMachine.transition
    python solver.py --run-tests
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
SOLUTIONS = HERE.parent
REPO = SOLUTIONS.parent / "AI4SE_Playground"
TASKS_FILE = SOLUTIONS.parent / "Assignments" / "missing_code.json"
ENV_FILE = SOLUTIONS / ".env"
PROMPTS_DIR = HERE / "prompts"
RESPONSES_DIR = HERE / "responses"
RESULTS_FILE = HERE / "results.json"
TEST_RESULTS_FILE = HERE / "test_results.txt"

MODEL = os.getenv("SOLVER_MODEL", "gpt-5-mini")
TOP_N = 5

sys.path.insert(0, str(SOLUTIONS / "Task_4"))
sys.path.insert(0, str(SOLUTIONS / "Task_3"))
import embedder   # noqa: E402  (Task 3)
import retriever  # noqa: E402  (Task 4)

SYSTEM_PROMPT = """You are an expert Python developer working in an existing code base.
You implement exactly ONE missing method.
Rules:
- Return ONLY the complete method definition: the `def` line, the given docstring and the body.
- Do not return the class, imports, decorators, tests or any explanation.
- Keep the exact signature that is given.
- Use only names that exist in the code base or the standard library (see the context).
- Answer with a single ```python code block."""


# --------------------------------------------------------------------------
# locating the stub in the target file
# --------------------------------------------------------------------------
def _find_method(tree: ast.Module, class_name: str, method: str) -> Optional[ast.FunctionDef]:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            candidates = [f for f in node.body
                          if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)) and f.name == method]
            stubs = [f for f in candidates if _is_stub(f)]
            return (stubs or candidates or [None])[0]
    return None


def _is_stub(func: ast.AST) -> bool:
    body = list(func.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    return all(isinstance(s, ast.Pass) or
               (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and s.value.value is Ellipsis)
               for s in body)


def _read(path: Path) -> Tuple[str, str]:
    """Return (source with \\n line endings, original newline)."""
    raw = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), newline


def stub_signature(path: Path, class_name: str, method: str) -> Optional[str]:
    """Decorators + ``def`` line(s) of the stub, as they are in the file."""
    source, _ = _read(path)
    func = _find_method(ast.parse(source), class_name, method)
    if func is None:
        return None
    lines = source.split("\n")
    start = min([func.lineno] + [d.lineno for d in func.decorator_list])
    end = max(func.lineno, func.body[0].lineno - 1)
    return textwrap.dedent("\n".join(lines[start - 1:end]))


# --------------------------------------------------------------------------
# prompt
# --------------------------------------------------------------------------
def build_task_text(task: Dict) -> str:
    """Textual task = the same text that is embedded for retrieval (Task 3/4)."""
    return embedder.task_query_text(task)


def build_prompt(task_text: str, signature: str, docstring: str, matches: List) -> str:
    context = "\n\n".join(
        f"### Context {i} (similarity {m.score:.2f})\n```python\n{m.chunk['text']}\n```"
        for i, m in enumerate(matches, 1))
    return f"""## Task
{task_text}

Implement this method (it currently has only `pass` as its body):
```python
{signature}
    {docstring}
```

## Relevant code from the repository
{context}

Return only the complete method definition with the docstring, in one ```python block."""


# --------------------------------------------------------------------------
# LLM call (the only place where the API key is used)
# --------------------------------------------------------------------------
def call_llm(prompt: str) -> Tuple[str, Dict]:
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE)
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(f"OPENAI_API_KEY not found (expected in {ENV_FILE})")
    from openai import OpenAI
    client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL") or None, max_retries=2, timeout=180)
    t0 = time.perf_counter()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
    )
    usage = response.usage
    info = {
        "model": response.model,
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "seconds": round(time.perf_counter() - t0, 1),
    }
    return response.choices[0].message.content or "", info


# --------------------------------------------------------------------------
# turning the answer into code and writing it into the file
# --------------------------------------------------------------------------
def extract_method(answer: str, method: str) -> str:
    """Pull the method definition (without decorators) out of the LLM answer."""
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", answer, flags=re.S)
    code = textwrap.dedent(blocks[0] if blocks else answer).strip("\n")
    tree = ast.parse(code)  # raises SyntaxError for invalid code
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method:
            lines = code.split("\n")
            return textwrap.dedent("\n".join(lines[node.lineno - 1:node.end_lineno]))
    raise ValueError(f"no definition of `{method}` in the answer")


def insert_method(path: Path, class_name: str, method: str, method_code: str) -> None:
    """Replace the stub (from its ``def`` line, decorators kept) with ``method_code``."""
    source, newline = _read(path)
    func = _find_method(ast.parse(source), class_name, method)
    if func is None:
        raise ValueError(f"{class_name}.{method} not found in {path}")
    if not _is_stub(func):
        raise ValueError(f"{class_name}.{method} is already implemented")
    lines = source.split("\n")
    indent = " " * func.col_offset
    new_lines = [indent + line if line.strip() else "" for line in method_code.split("\n")]
    lines[func.lineno - 1:func.end_lineno] = new_lines
    new_source = "\n".join(lines)
    ast.parse(new_source)  # the whole file must still be valid Python
    path.write_bytes(new_source.replace("\n", newline).encode("utf-8"))


# --------------------------------------------------------------------------
# one task
# --------------------------------------------------------------------------
def solve_task(task_text: str, file: str, class_name: str, method: str, docstring: str,
               index: "retriever.ChunkIndex", dry_run: bool = False, force: bool = False) -> Dict:
    """Retrieve top-5 chunks for ``task_text``, ask the LLM, write the method into ``file``."""
    name = f"{class_name}.{method}"
    target = REPO / file
    result: Dict = {"task": name, "file": file}

    source, _ = _read(target)
    func = _find_method(ast.parse(source), class_name, method)
    if func is None:
        return {**result, "status": "method not found in file"}
    if not _is_stub(func):  # done in an earlier run -> never call the API again for it
        return {**result, "status": "skipped: already implemented (no API call)"}
    signature = stub_signature(target, class_name, method)

    matches = index.search(task_text, n=TOP_N)
    result["retrieved"] = [{"id": m.chunk["id"], "score": round(m.score, 3)} for m in matches]
    prompt = build_prompt(task_text, signature, docstring, matches)
    PROMPTS_DIR.mkdir(exist_ok=True)
    (PROMPTS_DIR / f"{name}.md").write_text(f"# SYSTEM\n{SYSTEM_PROMPT}\n\n# USER\n{prompt}\n", encoding="utf-8")
    if dry_run:
        return {**result, "status": "dry-run (prompt saved, no API call)", "prompt_chars": len(prompt)}

    # cached answer?
    RESPONSES_DIR.mkdir(exist_ok=True)
    cache_file = RESPONSES_DIR / f"{name}.json"
    prompt_hash = hashlib.sha256((MODEL + SYSTEM_PROMPT + prompt).encode()).hexdigest()[:16]
    cached = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else None
    if cached and cached.get("prompt_hash") == prompt_hash and not force:
        answer, info = cached["answer"], {**cached["usage"], "cached": True}
    else:
        answer, info = call_llm(prompt)
        cache_file.write_text(json.dumps({"task": name, "prompt_hash": prompt_hash, "model": MODEL,
                                          "usage": info, "answer": answer}, indent=2, ensure_ascii=False),
                              encoding="utf-8")
    result["usage"] = info

    try:
        method_code = extract_method(answer, method)
        insert_method(target, class_name, method, method_code)
        result["status"] = "inserted"
        result["code"] = method_code
    except (SyntaxError, ValueError) as exc:
        result["status"] = f"failed: {exc}"
    return result


# --------------------------------------------------------------------------
# tests
# --------------------------------------------------------------------------
def run_tests() -> str:
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                          cwd=REPO / "playground", capture_output=True, text=True, encoding="utf-8")
    output = proc.stdout + proc.stderr
    TEST_RESULTS_FILE.write_text(output, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Implement missing methods via the RAG pipeline.")
    parser.add_argument("--dry-run", action="store_true", help="build prompts only, no API call, no file change")
    parser.add_argument("--only", type=str, default=None, help="Class.method to process")
    parser.add_argument("--force", action="store_true", help="ignore cached answers and call the API again")
    parser.add_argument("--run-tests", action="store_true", help="run the unit tests afterwards")
    parser.add_argument("--tests-only", action="store_true", help="only run the unit tests")
    args = parser.parse_args()

    if args.tests_only:
        print(run_tests()[-3000:])
        return

    tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    if args.only:
        tasks = [t for t in tasks if f"{t['class']}.{t['method']}" == args.only]
        if not tasks:
            raise SystemExit(f"no task named {args.only}")

    index = retriever.ChunkIndex()
    print(f"model: {MODEL} | tasks: {len(tasks)} | mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    previous = json.loads(RESULTS_FILE.read_text(encoding="utf-8")) if RESULTS_FILE.exists() else {}
    totals = {"api_calls": 0, "prompt_tokens": 0, "completion_tokens": 0}

    for task in tasks:
        docstring = task["docstring"].strip()
        res = solve_task(build_task_text(task), task["file"], task["class"], task["method"], docstring,
                         index, dry_run=args.dry_run, force=args.force)
        usage = res.get("usage", {})
        if usage and not usage.get("cached"):
            totals["api_calls"] += 1
            totals["prompt_tokens"] += usage.get("prompt_tokens") or 0
            totals["completion_tokens"] += usage.get("completion_tokens") or 0
        tag = " (cached answer)" if usage.get("cached") else ""
        print(f"- {res['task']:<34} {res['status']}{tag}")
        if not args.dry_run and not res["status"].startswith("skipped"):
            previous[res["task"]] = res

    if not args.dry_run:
        RESULTS_FILE.write_text(json.dumps(previous, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"API calls this run: {totals['api_calls']} | prompt tokens: {totals['prompt_tokens']} "
          f"| completion tokens: {totals['completion_tokens']}")
    if args.dry_run:
        print(f"prompts saved to {PROMPTS_DIR}")

    if args.run_tests:
        output = run_tests()
        print("\n" + "\n".join(output.strip().split("\n")[-15:]))
        print(f"full test output: {TEST_RESULTS_FILE}")


if __name__ == "__main__":
    main()
