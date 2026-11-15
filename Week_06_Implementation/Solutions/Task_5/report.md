# Task 5 – Solving coding tasks with the RAG pipeline

## Outputs

| File | What it is |
|---|---|
| `solver.py` | Python script: textual task → top-5 chunks → prompt → LLM → code written into the target file |
| `prompts/` | The exact prompt sent for each of the 10 tasks |
| `responses/` | The raw LLM answer for each task (+ token usage) |
| `results.json` | Status, retrieved chunks and inserted code for each task |
| `baseline_tests.txt` | Unit test run **before** (stubs only) |
| `test_results.txt` | Unit test run **after** the pipeline |
| `report.md` | This report |

The generated methods were written directly into the source files in `../../AI4SE_Playground/playground/playground/`.

## How the pipeline works

The main function is `solve_task(task_text, file, class_name, method, docstring, index)`:

1. **Input:** a textual task. For each entry of `missing_code.json` it is the location + the docstring, e.g. `playground/playground/orders.py | method: OrderStateMachine.transition` + `Return ``target`` if the transition is allowed, else raise.`
2. **Retrieval:** the task text is embedded with the same model as the chunks (Task 3), and the **top 5 chunks** are picked by cosine similarity (Task 4). Empty stubs are skipped.
3. **Prompt:** contains the task, the exact signature + docstring of the method (taken from the target file) and the 5 chunks with their full text (including the class context). The system prompt tells the model to return only the method definition. Example: `prompts/OrderStateMachine.transition.md`.
4. **LLM:** `gpt-5-mini` (one of the allowed models: good at code and cheap) via the OpenAI API.
5. **Writing the code:** the method is taken out of the ```` ```python ```` block, the stub is replaced from its `def` line (decorators such as `@property` are kept), the code is indented correctly and the whole file is checked to still be valid Python before it is saved.

Run: `python solver.py --run-tests` (all tasks + unit tests).

### Cost control

Because the API key is limited, the script was built so that no call is wasted:
- `--dry-run` builds all prompts without calling the API. The prompts were checked first.
- `--only Class.method` runs one task. One task was tried first before running the rest.
- Every answer is saved in `responses/`; methods that are already implemented are skipped **without** calling the API.
- There is no automatic re-asking when the answer is wrong. The result shows what the pipeline does in one try.

**Total usage: 10 API calls, ~9,800 prompt tokens and ~5,300 completion tokens** (completion tokens include the hidden reasoning of `gpt-5-mini`).

## Unit test results

| | Passed | Failed | Total |
|---|---|---|---|
| Before (stubs with `pass`) | 429 | 52 | 481 |
| **After the RAG pipeline** | **463** | **18** | 481 |

**34 of the 52 failing tests were fixed; 96 % of all tests pass.** All 10 answers were valid Python and were inserted.

### Results per method

| Method | Tests | Note |
|---|---|---|
| `OrderStatus.is_terminal` | ✅ all pass | |
| `Warehouse.stock_report` | ✅ all pass | |
| `Customer.can_afford` | ✅ all pass | |
| `Order.__len__` | ✅ all pass | |
| `Money.__bool__` | ✅ all pass | |
| `BulkDiscountPricing.price` | ❌ 8 fail | computes `Money // 100`, which `Money` does not support |
| `OrderStateMachine.transition` | ❌ 5 fail | raises `ValueError` instead of `InvalidTransitionError` |
| `InventoryLedger.__contains__` | ❌ 3 fail | raises an error for an invalid SKU instead of returning `False`; behaviour at zero stock differs |
| `EventBus.__contains__` | ❌ 1 fail | raises `TypeError` for a non-`EventType` instead of returning `False` |
| `OrderLog.by_status` | ❌ 1 fail | does not raise `TypeError` for an invalid status |

**5 of 10 methods are fully correct.** The other 5 have correct main logic but fail on details.

## Why the failures happened

**1. Retrieval did not provide the needed context (13 tests).**
- `BulkDiscountPricing.price`: the top 5 were the other methods of `BulkDiscountPricing`, but not the `Money` class. The model did not know that `Money` has no `//` operator and that the calculation must be done with `.cents`.
- `OrderStateMachine.transition`: the exception `InvalidTransitionError` (defined in `exceptions.py`, imported in `orders.py`) was not in the top 5, so the model used the general `ValueError`.

Embedding similarity finds code that *looks like* the task (sibling methods of the same class). It does not find what the code *depends on* (types, exceptions, imports), because that code does not look similar.

**2. The docstring is not a full specification (5 tests).** The edge cases are only defined in the tests, which the model did not see:
- `InventoryLedger.__contains__`: the docstring says "positive on-hand stock", but one test expects `True` even at zero stock after a commit, and others expect `False` (not an error) for invalid SKUs.
- `EventBus.__contains__`, `OrderLog.by_status`: the expected behaviour for a wrong argument type is not in the docstring. For `EventBus` the model copied the type check from `subscribe`.

## Conclusion

The RAG pipeline works: it implemented all 10 methods in one try each and **reduced failing tests from 52 to 18**. The remaining failures show the main weakness of pure embedding retrieval: it does not bring in the dependencies of the code (types, exceptions) and the tests that define the edge cases. Adding the imports/used classes of the target file and the related tests to the context would most likely fix most of them (see the bonus task).
