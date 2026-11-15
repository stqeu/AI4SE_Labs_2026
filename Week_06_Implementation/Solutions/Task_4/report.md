# Task 4 – Matching embeddings

## Outputs

| File | What it is |
|---|---|
| `retriever.py` | Python script that returns the *n* most relevant chunks for an input embedding |
| `retrieval_results.txt` | Top-5 chunks for each task from `missing_code.json` (written when the script is run) |
| `report.md` | This report |

Run: `python retriever.py` (top-5 for every missing method), `python retriever.py --query "some text" --n 3` (any query).

## How it works

```python
index = ChunkIndex()                          # loads ../Task_3/embeddings.npy + store.json
matches = index.top_n(query_embedding, n=5)   # embedding in  ->  5 best chunks out
matches = index.search("task text", n=5)      # same, but embeds the text first
```

1. The input embedding is normalised to length 1.
2. Similarity with all chunks at once: `scores = embeddings @ query`.
3. Chunks that should not be returned (stubs, optional filter by type) get the score −∞.
4. `np.argpartition` picks the *n* best, which are then sorted from the most similar.
5. Every result contains the score and the whole chunk (file, class, name, full text for the prompt).

## Design decisions

**Cosine similarity.** It is the standard measure for text embeddings and the `all-MiniLM-L6-v2` model was trained for it. It compares the direction of vectors, not their length, so a long and a short chunk about the same thing still come out as similar. The vectors are already normalised in Task 3, so cosine similarity is just a dot product.

**Exact search over all chunks (brute force), no approximate index.** There are only 729 vectors with 384 numbers each. Comparing a query with all of them is a single matrix multiplication and takes well under a millisecond. The results are exact. An approximate index (FAISS, HNSW, …) only pays off with hundreds of thousands of vectors and would add a dependency and some lost accuracy for nothing.

**`argpartition` instead of sorting everything.** It finds the *n* best in linear time; only these *n* are sorted afterwards.

**Stub methods are skipped (by default).** Empty methods (`pass`) carry no information. The stub of the very method being implemented would be the most similar chunk, but useless, and it would take one of the top-5 places.

**Optional filter by chunk type (`kinds`).** For example, only source code without tests. It is off by default: the check in Task 3 showed that tests do not crowd out source code in the top results (they are 515 of 729 chunks, but only a few of them show up near the top), and relevant tests are useful because they show the expected behaviour.

**The query is embedded with the same function as the chunks** (`embedder.embed_texts` from Task 3), so the query and the chunks are in the same vector space. For a missing method, the query is the location (file, class, method) + its docstring.

**n is a parameter** (default 5, as Task 5 requires).

## Results (top-5 for the 10 missing methods)

Full output: `retrieval_results.txt`.

- **For all 10 methods, the top-5 chunks come from the correct file and almost always from the correct class**: sibling methods, the class overview (`class_skeleton`) and the tests of that method.
- **Tests do not crowd out source code:** tests are 71 % of all chunks (515 of 729) but only **8 of the 50** returned chunks (16 %). They show up only where they test the method in question (e.g. `test_can_afford_*` for `Customer.can_afford`). That is why the filter by type is off by default.
- Examples of useful matches:
  - `OrderStateMachine.transition` → `can_transition` (0.856), `Order.advance` (calls `transition`), `__call__`, `TRANSITIONS`;
  - `OrderStatus.is_terminal` → the `OrderStatus` overview + three tests `test_*_is_terminal` that show the exact expected values;
  - `Order.__len__` → `OrderBuilder.__len__` (the same pattern in another class), `Order.items`, `Order.__iter__`.
- **Weaker case:** for `Money.__bool__`, all 5 results are other `Money` methods (`__init__`, `__le__`, …). This is correct and shows where the amount is stored, but no test of `__bool__` made it to the top-5. Embedding similarity prefers chunks that "look like" the class over chunks that describe the specific behaviour.
