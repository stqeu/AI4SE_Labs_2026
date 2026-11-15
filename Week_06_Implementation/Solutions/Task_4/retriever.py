"""Match a query embedding with the chunk store (Week 06, Task 4).

Given an input embedding, return the *n* most relevant chunks from the
storage built in Task 3 (``../Task_3/embeddings.npy`` + ``store.json``).

Matching = cosine similarity. All stored vectors are L2-normalised, so cosine
similarity is just a dot product: ``embeddings @ query``. Exact brute-force
search over all chunks is used (729 x 384 values, well under 1 ms), and
``np.argpartition`` picks the best n without sorting everything.

Filters:
* stub methods (body only ``pass``) are skipped by default - they carry no
  information and the empty stub of the method being implemented would
  otherwise be a near-perfect but useless match;
* optional ``kinds`` filter (e.g. only source code, no tests).

Usage:
    python retriever.py                 # top-5 for every task in missing_code.json
    python retriever.py --n 3
    python retriever.py --query "return True when the order is shipped"
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import numpy as np

HERE = Path(__file__).resolve().parent
TASK3_DIR = HERE.parent / "Task_3"
DEFAULT_TASKS = HERE.parent.parent / "Assignments" / "missing_code.json"

sys.path.insert(0, str(TASK3_DIR))
import embedder  # noqa: E402  (Task 3: embed_texts, load_store, task_query_text)


@dataclass
class Match:
    score: float   # cosine similarity, -1..1 (higher = more similar)
    chunk: Dict    # the chunk from store.json (id, file, kind, text, ...)


class ChunkIndex:
    """In-memory index over the Task 3 store."""

    def __init__(self, store_dir: Path = TASK3_DIR) -> None:
        self.vectors, self.store = embedder.load_store(store_dir)
        self.chunks: List[Dict] = self.store["chunks"]

    def top_n(self, query_vec: np.ndarray, n: int = 5, exclude_stubs: bool = True,
              kinds: Optional[Iterable[str]] = None) -> List[Match]:
        """Return the ``n`` chunks most similar to ``query_vec``, best first."""
        query = np.asarray(query_vec, dtype=np.float32).ravel()
        query = query / (np.linalg.norm(query) or 1.0)       # make sure it is unit length
        scores = self.vectors @ query                         # cosine similarity for every chunk

        allowed = np.ones(len(self.chunks), dtype=bool)
        if exclude_stubs:
            allowed &= np.array([not c["is_stub"] for c in self.chunks])
        if kinds is not None:
            kinds = set(kinds)
            allowed &= np.array([c["kind"] in kinds for c in self.chunks])
        scores = np.where(allowed, scores, -np.inf)

        n = min(n, int(allowed.sum()))
        if n <= 0:
            return []
        best = np.argpartition(-scores, n - 1)[:n]            # n best, unordered
        best = best[np.argsort(-scores[best])]                # order them
        return [Match(float(scores[i]), self.chunks[i]) for i in best]

    def search(self, text: str, n: int = 5, **kwargs) -> List[Match]:
        """Embed ``text`` with the same model as the chunks and return the top ``n``."""
        return self.top_n(embedder.embed_texts([text])[0], n=n, **kwargs)


def _format(matches: List[Match]) -> List[str]:
    return [f"    {m.score:.3f}  [{m.chunk['kind']}] {m.chunk['id']}" for m in matches]


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve the n most relevant chunks for a query.")
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--query", type=str, default=None, help="free-text query instead of missing_code.json")
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    args = parser.parse_args()

    index = ChunkIndex()
    lines: List[str] = []
    if args.query:
        lines.append(f"query: {args.query}")
        lines += _format(index.search(args.query, n=args.n))
    else:
        tasks = json.loads(args.tasks.read_text(encoding="utf-8"))
        for task in tasks:
            matches = index.search(embedder.task_query_text(task), n=args.n)
            lines.append(f"{task['file']} :: {task['class']}.{task['method']}")
            lines += _format(matches)
        (HERE / "retrieval_results.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
