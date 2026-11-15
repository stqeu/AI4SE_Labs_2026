"""Embed repository chunks and store chunk-embedding pairs (Week 06, Task 3).

Embedding model: ``sentence-transformers/all-MiniLM-L6-v2`` (local, CPU,
384-dimensional vectors). The course API key has no access to OpenAI
embedding models, so a local model is used.

What is embedded (``embedding_text``):
    "<file> | <kind>: <Class.name>\\n<code of the unit>"
i.e. the location header + the code of the method/function/test itself
(signature, docstring, body). The class context that Task 2 puts in front of
every method is NOT embedded: the model reads at most 256 tokens, and the
shared class header would push the method's own code out of that window and
make all methods of one class look alike. The full ``text`` (with context)
is still stored and is what goes into the LLM prompt later.

Storage (in this folder):
    embeddings.npy  float32 matrix [n_chunks x 384], L2-normalised rows
    store.json      metadata + list of chunks; chunk["row"] = its row
                    in embeddings.npy  ->  one chunk-embedding pair per row

Usage:
    python embedder.py            # embed chunks, write the store, run a sanity check
    python embedder.py --no-check
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
DEFAULT_CHUNKS = HERE.parent / "Task_2" / "chunks.json"
DEFAULT_TASKS = HERE.parent.parent / "Assignments" / "missing_code.json"
EMB_FILE = "embeddings.npy"
STORE_FILE = "store.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 32

_model = None


# --------------------------------------------------------------------------
# embedding
# --------------------------------------------------------------------------
def get_model():
    """Load the sentence-transformers model once (downloaded on first use, ~90 MB)."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME, device="cpu")
    return _model


def embed_texts(texts: Sequence[str], batch_size: int = BATCH_SIZE) -> np.ndarray:
    """Turn texts into L2-normalised float32 vectors (one row per text).

    The same function is used for chunks (Task 3) and for task queries
    (Task 4/5), so both live in the same vector space.
    """
    vectors = get_model().encode(list(texts), batch_size=batch_size,
                                 normalize_embeddings=True, show_progress_bar=False,
                                 convert_to_numpy=True)
    return vectors.astype(np.float32)


def embedding_text(chunk: Dict) -> str:
    """The representation of a chunk that gets embedded (see module docstring)."""
    location = f"{chunk['class_name']}.{chunk['name']}" if chunk.get("class_name") else chunk["name"]
    return f"{chunk['file']} | {chunk['kind']}: {location}\n{chunk['code']}"


def embed_chunk(chunk: Dict) -> np.ndarray:
    """Embedding of a single chunk (384 floats)."""
    return embed_texts([embedding_text(chunk)])[0]


def task_query_text(task: Dict) -> str:
    """Text used to embed one entry of missing_code.json."""
    docstring = task["docstring"].strip().strip('"').strip()
    return f"{task['file']} | method: {task['class']}.{task['method']}\n{docstring}"


# --------------------------------------------------------------------------
# storage
# --------------------------------------------------------------------------
def build_store(chunks: List[Dict], out_dir: Path) -> Tuple[np.ndarray, Dict]:
    texts = [embedding_text(c) for c in chunks]
    tokenizer = get_model().tokenizer
    max_len = get_model().max_seq_length
    n_truncated = sum(len(tokenizer.tokenize(t)) + 2 > max_len for t in texts)  # +2 = [CLS], [SEP]

    t0 = time.perf_counter()
    vectors = embed_texts(texts)
    seconds = time.perf_counter() - t0

    store_chunks = []
    for row, (chunk, text) in enumerate(zip(chunks, texts)):
        entry = dict(chunk)
        entry["row"] = row
        entry["embedding_text"] = text
        store_chunks.append(entry)

    store = {
        "model": MODEL_NAME,
        "dim": int(vectors.shape[1]),
        "normalized": True,
        "max_seq_length": max_len,
        "n_chunks": len(chunks),
        "n_truncated": n_truncated,
        "embed_seconds": round(seconds, 2),
        "embedding_file": EMB_FILE,
        "chunks": store_chunks,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / EMB_FILE, vectors)
    (out_dir / STORE_FILE).write_text(json.dumps(store, indent=2, ensure_ascii=False), encoding="utf-8")
    return vectors, store


def load_store(store_dir: Path = HERE) -> Tuple[np.ndarray, Dict]:
    """Load (embeddings, store) written by :func:`build_store`."""
    store = json.loads((store_dir / STORE_FILE).read_text(encoding="utf-8"))
    vectors = np.load(store_dir / store["embedding_file"])
    assert vectors.shape == (store["n_chunks"], store["dim"]), "store and embeddings do not match"
    return vectors, store


# --------------------------------------------------------------------------
# sanity check: are the right chunks close to each missing method?
# --------------------------------------------------------------------------
def sanity_check(vectors: np.ndarray, store: Dict, tasks: List[Dict], k: int = 3) -> List[str]:
    chunks = store["chunks"]
    queries = embed_texts([task_query_text(t) for t in tasks])
    scores = queries @ vectors.T  # cosine similarity (rows are normalised)
    lines = []
    for task, row_scores in zip(tasks, scores):
        order = [i for i in np.argsort(-row_scores) if not chunks[i]["is_stub"]][:k]
        hit = any(chunks[i]["class_name"] in (task["class"], task["class"] + "Tests") or
                  task["class"] in (chunks[i]["class_name"] or "") or
                  chunks[i]["name"] == task["class"] for i in order)
        lines.append(f"{task['class']}.{task['method']}  [{'class found' if hit else 'class NOT in top-' + str(k)}]")
        for i in order:
            lines.append(f"    {row_scores[i]:.3f}  {chunks[i]['id']}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Embed chunks and build the chunk-embedding store.")
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--out", type=Path, default=HERE)
    parser.add_argument("--no-check", action="store_true")
    args = parser.parse_args()

    chunks = json.loads(args.chunks.read_text(encoding="utf-8"))
    print(f"model: {MODEL_NAME}")
    vectors, store = build_store(chunks, args.out)
    print(f"embedded {store['n_chunks']} chunks -> {vectors.shape} in {store['embed_seconds']} s")
    print(f"chunks longer than {store['max_seq_length']} tokens (truncated): {store['n_truncated']}")
    print(f"written: {args.out / EMB_FILE}, {args.out / STORE_FILE}")

    if not args.no_check:
        tasks = json.loads(args.tasks.read_text(encoding="utf-8"))
        report = sanity_check(vectors, store, tasks)
        text = "\n".join(report)
        print("\nSanity check - top-3 non-stub chunks for each missing method:\n" + text)
        (args.out / "sanity_check.txt").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
