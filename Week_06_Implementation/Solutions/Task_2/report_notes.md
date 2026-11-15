# Task 2 – notes for the report (to be turned into report.md later)

## How it was done
- `chunker.py` was written and run with Claude (claude.ai chat linked to the PC); only the Python standard library (`ast`, `json`).
- Run: `python chunker.py` (defaults: repo = `../../AI4SE_Playground`, output = `chunks.json` next to the script).

## Splitting method: AST, not a fixed character/line window
- Python's `ast` module gives exact start/end lines of every class and function, so a chunk never cuts a function in half.
- Every chunk is a complete, meaningful code unit, and metadata (file, class, name, lines, docstring) comes for free.
- Rejected alternatives:
  - fixed windows of N characters/lines: they cut functions and classes in the middle, and the chunk loses the context of what it belongs to;
  - whole files: too coarse. Top-5 would mean ~5 whole files, and retrieval precision drops.

## Chunk size
- Not a fixed number: the size follows code boundaries; the granularity is **one method/function**.
- Reason: the Task 5 tasks are also "implement one method", so the unit of retrieval matches the unit of work.
- Statistics (approx. tokens = chars / 4):

| kind | count | avg tok | median | max |
|---|---|---|---|---|
| class_skeleton | 30 | 212 | 222 | 436 |
| function | 6 | 159 | 165 | 202 |
| method | 152 | 159 | 151 | 646 |
| module | 26 | 105 | 84 | 298 |
| test | 515 | 92 | 87 | 273 |
| **all** | **729** | **112** | **94** | **646** |

- Whole repository ≈ 81k tokens. Top-5 chunks ≈ 500–1500 tokens, so they easily fit into a prompt even for the small models (gpt-4.1-nano, gpt-5-nano).
- The largest chunk is `Simulation.step` (~646 tok). Even so, there was no need to split methods further.

## Chunk types (and why)
1. **method**: the method source + a compact **class header** in front of it:
   - class line, class docstring, class-level attributes (e.g. `TRANSITIONS`);
   - `__init__` signature + all `self.<attr> = ...` assignments.

   Why: without it the model doesn't know what `self._items`, `self._status` etc. are.
2. **class_skeleton**: one per class; signatures and docstrings of all methods without bodies (`...`). This is an overview of the class API: which helpers already exist and can be called (e.g. `can_transition` for `transition`). Missing methods are marked `# NOT IMPLEMENTED`.
3. **module**: module docstring, imports and constants. Shows types and dependencies.
4. **function**: module-level functions.
5. **test**: one test method / test helper from `tests/`, with the test class line. Why: tests show how a method is called and what it must return. That is the most precise specification available. (Note: they are part of the repo, so using them is legitimate.)

## Stub flag
- `is_stub=true` = the method body is only `pass`/`...`. Exactly the **10 methods from `missing_code.json`** were found.
- `@abstractmethod` methods in `base.py` (`Entity.identity`, `PricingStrategy.price`, `Repository.*`) are empty on purpose, so they are **not** marked as stubs. The first version flagged them by mistake (16 stubs); fixed by checking the decorator.
- Use: the empty stub carries no information, so it can be filtered out during retrieval (Task 4) so it doesn't take up a top-5 slot.

## Data structure
- `chunks.json` = a list of objects: `id, file, kind, class_name, name, start_line, end_line, is_stub, docstring, code, text, n_chars, approx_tokens`.
- `code` = raw source; `text` = header comment (`# file: … | method: … | lines …`) + context + code. That is the text for the prompt and for embedding.
- `file` is relative to the repo root (`playground/playground/orders.py`), so it matches the paths in `missing_code.json`.
- `__pycache__`, `.pytest_cache` and similar are skipped. CRLF line endings (Windows) are handled.

## Notes for later
- Note: the whole repo (~81k tokens) would fit into the context of current models. RAG is used here because of the assignment; this is a good point for the bonus as well.
- `chunks.json` must be generated from the **original** repo (before Task 5 writes generated code into it). Don't regenerate it afterwards.
- Possible improvement: tests are 515 of 729 chunks, so they can crowd out source chunks in top-5. Decide in Task 4 (e.g. filter by kind / quota).
