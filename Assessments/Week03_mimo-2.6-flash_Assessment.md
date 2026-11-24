# Assessment by mimo-2.6-flash

# Week 03 Prompting
- Awarded: 3b out of 5b
- Commentary: Tasks 1-3 are complete and well documented: three distinct frameworks with prompts and rationale, a clean comparison run with per-prompt metadata and measured inference times, and a genuinely useful new metric (Row Overlap F1) with working code and results. Task 4, worth a third of the grade, has no deliverable at all beyond the assignment description, so no statistical significance testing, factor analysis or detailed interpretation was submitted. Two PNG charts (accuracy.png, row_f1_chart.png) could not be opened in this grading session; they were judged only from the surrounding report text, which includes equivalent tables.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: Three frameworks (RTF, CO-STAR, CoT) were chosen from the required source (frompting.com/frameworks), none of them ROSES or zero-shot. All three prompt files exist in `prompts/` and are tailored to the Task 2 text-to-SQL problem with concrete constraints (two output columns, schema-only access, CSV output format). `report.md` states where each framework was found, why it was chosen, and the expected outcome for each (RTF as a weak baseline, CO-STAR for context-heavy schema work, CoT for hard questions at the cost of longer inference). All stated outputs are delivered.

## Task 2
- Awarded: 1b   (max 1b)
- Commentary: Predictions for all three prompts are stored under `data/<PROMPT>/restaurants_dataset_predictions.csv` (plus the CoT reasoning trace), each row carrying model and prompt metadata, and `runs.csv` records prompt, prompt file, model (Claude Opus 5.5), inference time, correct/total and accuracy. Inference times are measured (RTF 1:08, CO-STAR 1:19, CoT 2:03), the report documents a fresh session per prompt and a blinded input folder, and `report.md` contains a comparison table, interpretation and an embedded chart (`accuracy.png`; not viewable here, judged from the table). Results are internally consistent (147/155, 154/155, 154/155).

## Task 3
- Awarded: 1b   (max 1b)
- Commentary: The proposed metric, Row Overlap F1 over returned rows averaged per question, is well argued: it gives partial credit where exact match is binary, it is cheaply computable from the existing harness, and the report explicitly discusses that it complements rather than replaces exact-match accuracy. `row_f1.py` implements the metric (in-memory DB rebuild, Counter-based precision/recall/F1, error handling) and writes `results.csv` (RTF 0.9851, CO-STAR 0.9935, CoT 0.9935), matching the report. Extra artifacts (`results/per_question.csv`, `results/summary.csv`, a chart) add per-question detail, though no source file in the submission generates the `results/` folder — only `results.csv` is reproducible from the committed code, a minor gap.

## Task 4
- Awarded: 0b   (max 2b)
- Commentary: Only `Task_4.md` (the assignment text) exists; no report, tables, graphs or analysis was submitted. Nothing addresses the required statistical significance test (e.g., McNemar/paired test over the 155 questions), no deeper metric-value breakdown beyond what Task 3 already contained, and no discussion of prompts vs. model vs. coding agent as contributing factors. Since essentially all Task 4 requirements are unmet, no credit is awarded.