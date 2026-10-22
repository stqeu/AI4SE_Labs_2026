"""Deterministic text similarity (TF-IDF + cosine), pure Python.

Used by the Pre-dedup node (to group near-duplicate candidates before the
Consolidator sees them) and by the Validator (to flag duplicate final
requirements). No AI involved.
"""
from __future__ import annotations

import math
import re
from collections import Counter

_STOPWORDS = set("""
a an the and or of to in on for with by from as at be is are was were been it
its this that these those shall should must will would can could may might
system able allow allows allowing provide provides support supports user users
staff library libraries need needs want wants also any all each such than then
via into per not no only more most other some so when which who whom what how
""".split())

_TOKEN = re.compile(r"[a-z][a-z0-9]+")


def _stem(word: str) -> str:
    for suffix in ("ations", "ation", "ings", "ing", "ies", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[: -len(suffix)] + ("y" if suffix == "ies" else "")
    return word


def tokenize(text: str) -> list[str]:
    return [_stem(t) for t in _TOKEN.findall(text.lower()) if t not in _STOPWORDS]


def tfidf_vectors(texts: list[str]) -> list[dict[str, float]]:
    docs = [Counter(tokenize(t)) for t in texts]
    n = len(docs)
    df = Counter(term for d in docs for term in d)
    vectors = []
    for d in docs:
        vec = {t: (1 + math.log(c)) * math.log((1 + n) / (1 + df[t]) + 1)
               for t, c in d.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vectors.append({t: v / norm for t, v in vec.items()})
    return vectors


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(t, 0.0) for t, v in a.items())


def similar_pairs(texts: list[str], threshold: float) -> list[tuple[int, int, float]]:
    """All index pairs (i, j, score) with cosine similarity >= threshold."""
    vecs = tfidf_vectors(texts)
    pairs = []
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            s = cosine(vecs[i], vecs[j])
            if s >= threshold:
                pairs.append((i, j, s))
    return pairs


def cluster(texts: list[str], threshold: float) -> list[list[int]]:
    """Single-link clustering via union-find; returns groups of size >= 2."""
    parent = list(range(len(texts)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j, _ in similar_pairs(texts, threshold):
        parent[find(i)] = find(j)

    groups: dict[int, list[int]] = {}
    for i in range(len(texts)):
        groups.setdefault(find(i), []).append(i)
    return sorted((g for g in groups.values() if len(g) > 1),
                  key=lambda g: (-len(g), g[0]))


def top_k_similar(queries: list[str], targets: list[str], k: int = 1
                  ) -> list[list[tuple[int, float]]]:
    """For each query text, the k most similar target texts (index, score).
    IDF is computed over queries + targets together."""
    if not targets:
        return [[] for _ in queries]
    vecs = tfidf_vectors(queries + targets)
    qv, tv = vecs[:len(queries)], vecs[len(queries):]
    out = []
    for q in qv:
        scored = sorted(((j, cosine(q, t)) for j, t in enumerate(tv)),
                        key=lambda x: -x[1])
        out.append(scored[:k])
    return out
