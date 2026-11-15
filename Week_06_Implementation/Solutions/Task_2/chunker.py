"""AST-based chunker for the AI4SE_Playground repository (Week 06, Task 2).

Splits every ``*.py`` file of the repository into chunks that follow code
boundaries instead of a fixed character window:

* ``method``          - one method of a class, prefixed with a compact class
                        header (class line, class docstring, class attributes,
                        and the ``self.<attr>`` assignments from ``__init__``)
* ``function``        - one module-level function
* ``class_skeleton``  - one per class: header + signatures and docstrings of
                        all methods, without bodies (overview of the class API)
* ``module``          - module docstring, imports and module-level constants
* ``test``            - one test method / test helper function from ``tests/``

Methods whose body is only ``pass`` (the missing methods of the assignment)
are marked ``is_stub=True`` so that retrieval can skip them later. Abstract
methods (``@abstractmethod``) are empty on purpose and are not stubs.

Only the standard library is used.

Usage:
    python chunker.py [--repo PATH] [--out PATH]
"""
from __future__ import annotations

import argparse
import ast
import json
import statistics
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
DEFAULT_REPO = HERE.parent.parent / "AI4SE_Playground"
DEFAULT_OUT = HERE / "chunks.json"
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".git", ".venv", "venv"}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _start_line(node: ast.AST) -> int:
    """First line of a node, including its decorators."""
    decorators = getattr(node, "decorator_list", [])
    return min([node.lineno] + [d.lineno for d in decorators])


def _segment(lines: List[str], start: int, end: int) -> str:
    """Source lines ``start..end`` (1-based, inclusive)."""
    return "\n".join(lines[start - 1:end])


def _docstring_node(node: ast.AST) -> Optional[ast.Expr]:
    body = getattr(node, "body", [])
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        return body[0]
    return None


def _is_abstract(func: ast.AST) -> bool:
    """True for ``@abstractmethod`` (an intentionally empty body, not a missing one)."""
    for dec in getattr(func, "decorator_list", []):
        name = dec.attr if isinstance(dec, ast.Attribute) else getattr(dec, "id", "")
        if name == "abstractmethod":
            return True
    return False


def _is_stub(func: ast.AST) -> bool:
    """True when the body is only ``pass`` / ``...`` and the method is not abstract."""
    if _is_abstract(func):
        return False
    body = list(func.body)
    if _docstring_node(func) is not None:
        body = body[1:]
    if not body:
        return True
    for stmt in body:
        if isinstance(stmt, ast.Pass):
            continue
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
            continue
        return False
    return True


def _signature(lines: List[str], func: ast.AST) -> str:
    """Decorators + ``def`` line(s) of a function, without the body."""
    start = _start_line(func)
    first_body = func.body[0]
    end = max(func.lineno, first_body.lineno - 1)
    sig = _segment(lines, start, end)
    if first_body.lineno == func.lineno:  # one-line def: cut the body off
        sig = sig.split(":", 1)[0] + ":"
    return sig


def _approx_tokens(text: str) -> int:
    """Rough token estimate (~4 characters per token for code)."""
    return max(1, round(len(text) / 4))


# --------------------------------------------------------------------------
# class context
# --------------------------------------------------------------------------
def _class_header(lines: List[str], cls: ast.ClassDef) -> str:
    """Compact class context used in front of every method chunk."""
    parts = [_segment(lines, _start_line(cls), cls.lineno)]
    doc = _docstring_node(cls)
    if doc is not None:
        parts.append(_segment(lines, doc.lineno, doc.end_lineno))
    # class-level attributes / constants
    for stmt in cls.body:
        if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
            parts.append(_segment(lines, stmt.lineno, stmt.end_lineno))
    # attributes set in __init__ (tells the model what ``self`` holds)
    for stmt in cls.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)) and stmt.name == "__init__":
            parts.append(_signature(lines, stmt))
            attr_lines = []
            for sub in ast.walk(stmt):
                if isinstance(sub, (ast.Assign, ast.AnnAssign)):
                    targets = sub.targets if isinstance(sub, ast.Assign) else [sub.target]
                    if any(isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
                           and t.value.id == "self" for t in targets):
                        attr_lines.append(_segment(lines, sub.lineno, sub.end_lineno))
            if attr_lines:
                indent = " " * (stmt.col_offset + 4)
                parts.append(f"{indent}# attributes set in __init__:")
                parts.extend(attr_lines)
            break
    return "\n".join(parts)


def _class_skeleton(lines: List[str], cls: ast.ClassDef) -> str:
    """Class header + every method signature and docstring, bodies replaced by ``...``."""
    parts = [_segment(lines, _start_line(cls), cls.lineno)]
    doc = _docstring_node(cls)
    if doc is not None:
        parts.append(_segment(lines, doc.lineno, doc.end_lineno))
    for stmt in cls.body:
        if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
            parts.append(_segment(lines, stmt.lineno, stmt.end_lineno))
        elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parts.append(_signature(lines, stmt))
            indent = " " * (stmt.col_offset + 4)
            mdoc = _docstring_node(stmt)
            if mdoc is not None:
                parts.append(_segment(lines, mdoc.lineno, mdoc.end_lineno))
            parts.append(f"{indent}...  # NOT IMPLEMENTED" if _is_stub(stmt) else f"{indent}...")
    return "\n".join(parts)


# --------------------------------------------------------------------------
# chunking of one file
# --------------------------------------------------------------------------
def chunk_file(path: Path, repo: Path) -> List[Dict]:
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    tree = ast.parse(source, filename=str(path))
    rel = path.relative_to(repo).as_posix()
    is_test = "tests" in path.relative_to(repo).parts or path.name.startswith("test_")
    chunks: List[Dict] = []

    def add(kind: str, name: str, class_name: Optional[str], start: int, end: int,
            code: str, context: str = "", is_stub: bool = False, docstring: Optional[str] = None) -> None:
        location = f"{class_name}.{name}" if class_name else name
        header = f"# file: {rel} | {kind}: {location} | lines {start}-{end}"
        body = f"{context}\n    ...\n{code}" if context else code
        chunks.append({
            "id": f"{rel}::{kind}::{location}",
            "file": rel,
            "kind": kind,
            "class_name": class_name,
            "name": name,
            "start_line": start,
            "end_line": end,
            "is_stub": is_stub,
            "docstring": docstring,
            "code": code,
            "text": f"{header}\n{body}",
        })

    # module-level code (docstring, imports, constants, __all__, ...)
    module_parts = []
    first, last = None, None
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        module_parts.append(_segment(lines, _start_line(stmt), stmt.end_lineno))
        first = first or _start_line(stmt)
        last = stmt.end_lineno
    if module_parts:
        add("module", path.stem, None, first, last, "\n".join(module_parts),
            docstring=ast.get_docstring(tree))

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add("test" if is_test else "function", node.name, None, _start_line(node), node.end_lineno,
                _segment(lines, _start_line(node), node.end_lineno),
                is_stub=_is_stub(node), docstring=ast.get_docstring(node))

        elif isinstance(node, ast.ClassDef):
            if not is_test:
                add("class_skeleton", node.name, None, _start_line(node), node.end_lineno,
                    _class_skeleton(lines, node), docstring=ast.get_docstring(node))
            header = _class_header(lines, node) if not is_test else \
                _segment(lines, _start_line(node), node.lineno)
            for item in node.body:
                if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                start = _start_line(item)
                add("test" if is_test else "method", item.name, node.name, start, item.end_lineno,
                    _segment(lines, start, item.end_lineno), context=header,
                    is_stub=_is_stub(item), docstring=ast.get_docstring(item))
    return chunks


def _dedupe_ids(chunks: List[Dict]) -> None:
    """Make ids unique (e.g. a property getter and setter share a name)."""
    seen: Dict[str, int] = {}
    for chunk in chunks:
        base = chunk["id"]
        if base in seen:
            seen[base] += 1
            chunk["id"] = f"{base}#{seen[base]}"
        else:
            seen[base] = 0


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def chunk_repository(repo: Path) -> List[Dict]:
    files = sorted(p for p in repo.rglob("*.py") if not SKIP_DIRS.intersection(p.parts))
    chunks: List[Dict] = []
    for path in files:
        chunks.extend(chunk_file(path, repo))
    _dedupe_ids(chunks)
    for chunk in chunks:
        chunk["n_chars"] = len(chunk["text"])
        chunk["approx_tokens"] = _approx_tokens(chunk["text"])
    return chunks


def print_stats(chunks: List[Dict]) -> None:
    print(f"total chunks: {len(chunks)}")
    by_kind: Dict[str, List[int]] = {}
    for c in chunks:
        by_kind.setdefault(c["kind"], []).append(c["approx_tokens"])
    print(f"{'kind':<16}{'count':>6}{'avg tok':>9}{'median':>8}{'max tok':>9}")
    for kind, toks in sorted(by_kind.items()):
        print(f"{kind:<16}{len(toks):>6}{statistics.mean(toks):>9.0f}{statistics.median(toks):>8.0f}{max(toks):>9}")
    all_toks = [c["approx_tokens"] for c in chunks]
    print(f"{'ALL':<16}{len(all_toks):>6}{statistics.mean(all_toks):>9.0f}"
          f"{statistics.median(all_toks):>8.0f}{max(all_toks):>9}")
    print(f"total approx tokens: {sum(all_toks)}")
    stubs = [c["id"] for c in chunks if c["is_stub"]]
    print(f"stub methods (body is only `pass`): {len(stubs)}")
    for s in stubs:
        print(f"  - {s}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO, help="repository root")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output JSON file")
    args = parser.parse_args()

    repo = args.repo.resolve()
    chunks = chunk_repository(repo)
    args.out.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"repo: {repo}\nwritten: {args.out}")
    print_stats(chunks)


if __name__ == "__main__":
    main()
