# Task 2 – Chunking the repository

The script and this report were generated with an LLM coding assistant (Claude).

## Outputs

| File | What it is |
|---|---|
| `chunker.py` | Python script that splits the repository into chunks (standard library only) |
| `chunks.json` | Data structure with all chunks (729 chunks) |
| `report.md` | This report |

Run: `python chunker.py` (default input: `../../AI4SE_Playground`, default output: `chunks.json`).

## Splitting method: by code structure (AST)

The repository is Python, so it is split with Python's `ast` module, not by a fixed number of characters or lines.

- `ast` gives the exact start and end line of every class and function, so **a chunk never cuts a function in half**.
- Every chunk is a complete code unit with useful metadata: file, class, name, lines and docstring.
- **Rejected alternatives:**
  - *fixed windows of N characters/lines*: they cut code in the middle and lose the information about which class the code belongs to;
  - *whole files*: too coarse. The top-5 retrieved chunks would be 5 whole files, which makes retrieval less precise.

## Chunk size: one method/function

The chunk size is not a fixed number; it follows code boundaries. **One chunk = one method or function.** This matches the coding tasks in Task 5, which are all "implement one method".

| kind | count | avg tokens | median | max |
|---|---|---|---|---|
| method | 152 | 159 | 151 | 646 |
| class_skeleton | 30 | 211 | 216 | 436 |
| module | 26 | 105 | 84 | 298 |
| function | 6 | 159 | 165 | 202 |
| test | 515 | 92 | 87 | 273 |
| **all** | **729** | **112** | **94** | **646** |

*(tokens ≈ characters / 4)*

Chunks are small, so the top 5 chunks take only about 500–1,500 tokens and fit into a prompt even for the smallest allowed models. The largest chunk (`Simulation.step`, ~650 tokens) still did not need further splitting.

## Chunk types

1. **method**: the method code plus a short **class header** in front of it. The header contains the class line, class docstring, class attributes and everything `__init__` stores on `self`. Without it, the model would not know what fields like `self._items` or `self._status` are.
2. **class_skeleton**: one per class, listing all method signatures and docstrings without bodies. It shows which methods of a class already exist and can be called (e.g. `can_transition` when implementing `transition`).
3. **module**: module docstring, imports and constants, which show the types and dependencies.
4. **function**: functions defined outside classes.
5. **test**: one test method from `tests/`. Tests show how a method is called and what it must return, which is the most precise specification available in the repository.

## Missing methods (`is_stub`)

Methods whose body is only `pass` are marked `is_stub: true`. The chunker found exactly the **10 methods listed in `missing_code.json`**. The abstract methods in `base.py` are empty on purpose, so methods with `@abstractmethod` are not counted as stubs. An empty stub carries no information, so it can be filtered out during retrieval.

## Data structure

`chunks.json` is a list of objects with these fields:

`id, file, kind, class_name, name, start_line, end_line, is_stub, docstring, code, text, n_chars, approx_tokens`

- `code`: the raw source code of the unit.
- `text`: a header line (`# file: … | method: … | lines …`) + context + code. This is what gets embedded (Task 3) and put into the prompt (Task 5).
- `file` is relative to the repository root (e.g. `playground/playground/orders.py`), the same format as in `missing_code.json`.
- Cache folders (`__pycache__`, `.pytest_cache`) are skipped.

## Note

The whole repository is only about 81k tokens and would fit into the context window of current models. The RAG pipeline is built because the assignment asks for it. With large repositories, chunking and retrieval are necessary.
