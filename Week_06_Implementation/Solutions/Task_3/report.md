# Task 3 – Embeddings and storage

## Outputs

| File | What it is |
|---|---|
| `embedder.py` | Python script that turns a chunk into an embedding and builds the storage |
| `embeddings.npy` | Embeddings of all 729 chunks: a 729 × 384 float32 matrix |
| `store.json` | The chunks with metadata; `chunk["row"]` is the row of its embedding in `embeddings.npy` |
| `sanity_check.txt` | Quality check: the most similar chunks for each missing method |
| `report.md` | This report |

Run: `python embedder.py` (reads `../Task_2/chunks.json`, writes into this folder).

## Embedding mechanism: local model `all-MiniLM-L6-v2`

- We first tried OpenAI `text-embedding-3-small`. The course API key returned **403 – the project has no access to this model**. The key only allows the chat models listed in the assignment.
- So a **local model** from the `sentence-transformers` library is used: `all-MiniLM-L6-v2`.
  - It produces **384-dimensional vectors** (the "few hundred numbers" from the assignment).
  - It runs on the CPU. All 729 chunks were embedded in **3.9 seconds**.
  - It is free, works offline, needs no API key and the code never leaves the computer.
  - It is one of the most widely used general-purpose embedding models and is small (~90 MB).
- **Downside:** it was trained mostly on natural language, not code. It still works well here because every chunk contains names, docstrings and a location header in normal words (see the quality check below).

## What part of the chunk is embedded

The embedded text is the **location header + the code of the unit itself**:

```
playground/playground/orders.py | method: OrderStateMachine.can_transition
def can_transition(self, source, target) -> bool:
    """Return whether ``target`` is reachable from ``source``."""
    ...
```

- **The class context from Task 2 is not embedded**: the class header and the `__init__` attributes that are put in front of every method. Reasons:
  1. the model reads at most **256 tokens**. A long class header would use up that space and the method's own code would be cut off;
  2. all methods of one class share the same header, so their vectors would become too similar and retrieval could not tell them apart.
- The full text with the context is still stored in `store.json` and is what goes into the LLM prompt in Task 5. **Embedding is for finding the chunk, the full text is for using it.**
- 19 of 729 chunks are longer than 256 tokens, and the model only reads their beginning. These are mostly class overviews (`class_skeleton`). The beginning still contains the class name, its docstring and the first methods, which is enough to find them.
- Stub methods (empty `pass`) are embedded too, but keep their `is_stub` flag so that retrieval can skip them.

## Vectors are normalised

All vectors are scaled to length 1. Cosine similarity then becomes a simple dot product (`query @ embeddings.T`), which makes the matching in Task 4 simple and fast.

## Storage: `.npy` + JSON, no vector database

- `embeddings.npy`: one NumPy matrix, loaded in milliseconds (1.1 MB).
- `store.json`: the chunks (id, file, class, name, lines, `is_stub`, code, full text, embedded text) and the model information (model name, dimension, normalisation).
- **The pairs are linked by row number:** chunk with `row = i` ↔ `embeddings[i]`.
- `load_store()` loads both and checks that they match.
- **Why no vector database** (FAISS, Chroma, …): with 729 vectors, comparing a query with all of them takes under a millisecond. A database would add a dependency and complexity without any benefit. For a repository with hundreds of thousands of chunks, an index like FAISS would make sense.
- The same `embed_texts()` function is used for chunks and for task descriptions (Task 4/5), so both are in the same vector space.

## Quality check

For each of the 10 missing methods from `missing_code.json`, the docstring was embedded and compared with all non-stub chunks. **For all 10 methods, the top 3 contain chunks of the correct class.** Examples (cosine similarity):

| Missing method | Top chunk | Score |
|---|---|---|
| `OrderStateMachine.transition` | `OrderStateMachine.can_transition` | 0.856 |
| `OrderStatus.is_terminal` | `OrderStatus` class overview | 0.775 |
| `Customer.can_afford` | `Customer.charge` (which calls `can_afford`) | 0.797 |
| `Order.__len__` | `OrderBuilder.__len__` (same pattern), then `Order.items` | 0.869 |

The retrieved chunks are the ones a programmer would look at: sibling methods of the same class, the class overview and related tests. Full results are in `sanity_check.txt`.
