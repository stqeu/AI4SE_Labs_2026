# Run log: requirements-refinement agentic network

This log records every **real** (paid) run of the network on the example corpus
`../data/corpus` (20 documents): what was run, what came out, what went wrong,
and what was changed before the next run. Free mock and offline test runs
are not listed individually.

Costs are calculated from the token counts printed by `main.py`. They use public
list prices per million tokens: gpt-5-mini $0.25 in / $2.00 out, gpt-5.6-luna
$0.20 / $1.20, gpt-6-luna $0.10 / $0.50.

---

## Run 1: 2026-10-20 (original design, one Consolidator call)

**Network:** loader → Extractor ×20 (parallel) → pre-dedup → Consolidator
(one call over *all* candidates) → validator → Reviewer → loop back to the
Consolidator (full rewrite) → renderer. Max 3 rounds.

**Command:** `python main.py --input ..\data\corpus`

| | |
|---|---|
| Candidates extracted | 702 (96% with verbatim evidence) |
| Requirements in document | **12** |
| Blacklisted | 3 |
| Candidates accounted for | **109 of 702 (16%)** |
| Review | 3 rounds, not approved |
| Time | 668 s |
| Tokens | gpt-5-mini 22 calls 57,629 in / 149,097 out · gpt-5.6-luna 3 calls 152,964 / 18,193 · gpt-6-luna 3 calls 100,735 / 15,753 |
| Cost | ≈ **$0.38** |

**What went wrong:** the Consolidator received all 702 candidates (about 80k tokens)
in a single call. It produced a handful of catch-all requirements
(for example "Management Roles And Responsibilities") and silently dropped 84% of
the candidates. Each revision round rewrote everything in one call again, so
the loop could not recover (6 → 10 → 12 requirements). The Reviewer correctly
refused approval each time and named the lost needs.

**Verdict:** the network works mechanically, but the output fails completeness (OS8),
duplicates (OS3) and consistency (OS7).

---

## Changes after Run 1: redesign of consolidation (2026-10-22)

**Kept unchanged, because it was judged correct:** Extractor (prompt, model, 12k-char
chunking; its cache stays valid), loader, pre-dedup, LLM client, renderer
layout, CLI with confirmation prompt, Reviewer instructions.

**Changed:**

| # | Change | Where | Spec |
|---|---|---|---|
| 1 | New **Planner** LLM node: sorts all candidates into ~20 topics and writes one shared glossary | `nodes/llm.py` `planner_node`, `prompts.py` `PLANNER_*` | OS3, OS7 |
| 2 | Deterministic **plan repair**: forgotten candidates go to the most similar topic, near-duplicates stay together, tiny topics are merged, large topics split (max 60) | `nodes/deterministic.py` `repair_plan` | OS8, OS3 |
| 3 | **Consolidator once per topic**, in parallel (`Send`), plus one automatic repair call if a candidate is left out | `consolidator_node`, `call_complete` | OS8 |
| 4 | New **Assembler** node joins the topic results; topic names become the document sections | `assembler_node` | OS7 |
| 5 | Validator: new checks for a candidate used twice and for catch-all requirements (more than 15 candidates) | `validate` | OS3 |
| 6 | **Reviser** replaces the full-rewrite revision: only the requirements named in issues are revised, in size-capped work packages | `reviser_node`, `build_packages` | ANS3, OS8 |
| 7 | Reviewer sees each requirement with its merged candidates; issues get major/minor severity; approval rule = no major reviewer issue and no blocking validator finding | `reviewer_node`, `prompts.py` | OS3, OS8 |
| 8 | `--mock` reads the real extraction cache read-only, so the free test exercises real data | `main.py` | – |

**Tests (free):** offline tests on the real 702 candidates; `main.py --mock` on
the real LangGraph. All 702 candidates were accounted for exactly once, and all
loop exits worked. Three bugs were found and fixed before any paid run:
single-item issues crashed packaging, revision packages had no size cap, and a
fragmented plan could create 100+ calls.

---

## Run 2: 2026-10-22 (topic-based consolidation, clean slate)

**Command:** `Rename-Item out out_run1` then `python main.py --input ..\data\corpus`
(no cache, so all three models are visibly used in one run).

| | |
|---|---|
| Candidates extracted | 609 (97% with verbatim evidence) |
| Topics (planner) | 19 topics, 19 batches of 13–60 candidates. Repair fixed 27 forgotten and 40 double-assigned IDs |
| Requirements in document | **260** (211 functional, 21 non-functional, 28 constraints) |
| Blacklisted | 40 (37 out of scope, 2 nonsensical, 1 conflict) |
| Candidates accounted for | **609 of 609 (100%)**, none used twice |
| Largest merge | 11 candidates (no catch-alls); 109 requirements combine several documents |
| Wording | 257/260 start with "The system shall"; descriptions average 54 words; 17-term glossary |
| Review | major issues 9 → 9 → 3; stopped at 3 rounds, not approved |
| Time | 798 s |
| Tokens | gpt-5-mini 23 calls 66,740 in / 154,221 out · gpt-5.6-luna 28 calls 167,176 / 92,532 · gpt-6-luna 3 calls 96,881 / 25,347 |
| Cost | ≈ **$0.49** (gpt-5-mini $0.33, gpt-5.6-luna $0.14, gpt-6-luna $0.02) |

**What worked:** completeness, no duplicates by shared candidates, no catch-alls,
consistent sections and wording, tracing, priorities, and a working review loop. All
three models were used in one run.

**Defects found:**

1. **Part of the SRS draft was never extracted.** `early_draft_srs_galecia.txt`
   part 2 of 3 (sections 9–14: Demographics, Inventory Control, Patron
   Records, Transaction Records, Financial Records, Report Types) hit the
   Extractor's 16,000-token output limit and was dropped. D10 gave 126 candidates
   against 195 in Run 1, so about 70 statements were missing. The incomplete
   result was also **saved to the cache**, so a plain re-run would have reused the gap.
   The downstream completeness checks could not see it, because they only know
   extracted candidates.
2. **Valid needs were discarded as "out of scope" because they seemed to belong to
   another topic.** About 24 of the 40 blacklist entries were wrongly discarded,
   for example "Weeding Reports", "Spreadsheet Export", "Export Inactive Patron CSV"
   and "Save And Reuse Reports", with explanations like "belongs to the Report
   Delivery topic". Cause: the Consolidator prompt said "other topics are handled
   separately", which the model read as permission to discard.
3. Minor, acceptable: 3 major review issues remained at the round limit
   (FR-036/FR-055 duplicate, FR-070 bundles three reports, BL-031 wrongly
   discarded). They are listed in section 9 of the document.

Output preserved as `out_run2/` (see Run 3 instructions).

---

## Changes after Run 2: fixes for Run 3 (only what is necessary)

### Fix 1: no lost document parts, no cached gaps (defect 1)

| Change | File |
|---|---|
| Extractor output ceiling raised from 16,000 to **32,000** tokens (includes reasoning tokens) | `config.py` `max_tokens_extractor` |
| The Extractor now counts failed parts. A document with a failed part is **not written to the cache**, and the log prints `WARNING: n part(s) failed, result NOT cached` | `nodes/llm.py` `extract_document_checked`, `extractor_node` |

The ceiling is not part of the cache key, so the 19 correctly cached documents
stay valid (cache keys verified unchanged). Only the bad D10 cache file must be
deleted by hand (see below).

### Fix 2: fitting another topic is never a reason to discard (defect 2)

| Change | File |
|---|---|
| Consolidator rule E rewritten: a candidate that fits another topic is kept as a requirement; fitting another topic is never a discard reason (cross-topic duplicates are merged later) | `prompts.py` `CONSOLIDATOR_SYSTEM` |
| Same rule added to the Reviser | `prompts.py` `REVISER_SYSTEM` |
| New validator check: an `out_of_scope` discard must explain why it is not about the software (project, meeting, documentation, process…). Otherwise it is a **major, blocking** finding, so the Reviser must restore it and approval is impossible while it remains | `nodes/deterministic.py` `_wrong_topic_discard`; `nodes/llm.py` blocking set |
| Blocking now requires severity *major* (the short-explanation check stays minor and non-blocking) | `nodes/llm.py` `reviewer_node` |

Check against the Run 2 blacklist: the new check flags 24 entries, the wrongly
discarded software needs including BL-031, which the Reviewer had also flagged.
It keeps all 13 genuine non-software discards (project tasks, meetings, SRS-writing
conventions).

**Not changed (deliberately):** planner, topic sizes, review rounds, the other
prompts. They behaved correctly in Run 2.

**Tests (free):** cache keys unchanged; a simulated truncated part is reported
and not cached; full `--mock` run on the real LangGraph graph passes.

---

## Run 3: 2026-10-22 (fixes applied; FINAL)

**Commands:** `Copy-Item out out_run2 -Recurse`, then `Remove-Item
out\cache\D10_c321539eef15cb4c.json`, then `python main.py --input ..\data\corpus`.
The preview showed `(20 documents, 19 cached)` and `3 extraction`, as intended.

| | |
|---|---|
| Extraction | 19 documents from cache; D10 re-extracted completely: **231 candidates** (was 126), no `FAILED` line, complete result cached |
| Candidates extracted | 714 (D10 now contributes 231) |
| Topics (planner) | 22 topics in 24 batches of 8–49. Repair fixed 6 forgotten and 269 double-assigned IDs |
| Requirements in document | **308** (250 functional, 26 non-functional, 32 constraints); 188 trace to the SRS |
| Blacklisted | **13**: 8 out of scope (all project/process/meeting items), 3 conflicts, 2 nonsensical. **0 wrong-topic discards** |
| Candidates accounted for | **714 of 714 (100%)**, none used twice, no unknown IDs |
| Largest merge | 10 candidates; 147 requirements combine several documents; all 20 documents covered |
| Wording | 308/308 start with "The system shall"; descriptions at least 34 words (mean 51); 22 sections; 20-term glossary |
| Priorities | Must 145, Should 141, Could 21, Won't 1 |
| Review | major issues 10 → 15 → 5; validator findings 9 → 0 → 0; stopped at 3 rounds, not approved |
| Time | 751 s |
| Tokens | gpt-5-mini 3 calls 9,337 in / 30,381 out · gpt-5.6-luna 33 calls 200,436 / 99,789 · gpt-6-luna 3 calls 104,258 / 23,333 |
| Cost | ≈ **$0.25** (gpt-5-mini $0.06, gpt-5.6-luna $0.16, gpt-6-luna $0.02) |

**Both fixes confirmed:**
- Fix 1: the SRS is fully extracted (231 candidates) and its complete result is cached.
- Fix 2: the blacklist dropped from 40 to 13 entries. Every remaining entry has a
  valid reason, and the validator's new check finds no wrong-topic discard.
  The conflicts are real contradictions resolved in favour of later decisions
  (e.g. the 2009 subcommittee's configuration migration and the survey's real-time reporting).

**Remaining open issues (listed in section 9 of `out/requirements.md`):** 5 major
items reported by the Reviewer in the last round:
- an architecture tension between reporting on the primary database
  (CON-019) and a replica/warehouse (CON-023, FR-174), which is also a tension present in the source documents;
- one duplicate (FR-016 / FR-149);
- three partially covered details (full field access, sharing saved queries,
  status-based inactive patrons).

There are also 3 minor wording findings. No validator (structural) issues remain.

**Verdict:** final run. Every network spec (ANS1–5) is implemented, and every output
spec (OS1–OS9) is met or addressed with the remaining gaps documented in the
output, which the assignment allows. Another run would not guarantee approval,
because each round surfaces new fine-grained findings, so the cost is not justified.

**Total spend on real runs:** ≈ $0.38 + $0.49 + $0.25 = **≈ $1.12** (plus a few
cents for the setup check and two single-document extractor tests).

**Final deliverable:** `out/requirements.md` (with `out/requirements.json` and
`out/graph.mmd`). Earlier runs are kept in `out_run1/` and `out_run2/`.
