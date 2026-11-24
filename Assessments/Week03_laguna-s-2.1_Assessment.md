# Assessment by laguna-s-2.1

# Week 03 Prompting
- Awarded: 3b out of 5b
- Commentary: Tasks 1-3 were completed thoroughly and correctly: three distinct prompting frameworks (RTF, CO-STAR, CoT) were selected from frompting.com, their prompts produced high-accuracy text-to-SQL predictions with measured inference times, and an original "Row Overlap F1" metric was implemented and compared across prompts. Task 4 has no deliverable present beyond the assignment description, so no report, tables, graphs, or statistical-significance analysis was provided to assess. Images (accuracy.png, row_f1_chart.png) could not be viewed by this model and were judged from the accompanying text and CSV data.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: Three distinct frameworks (RTF, CO-STAR, CoT) were chosen from https://frompting.com/frameworks, deliberately avoiding ROSES and zero-shot as instructed. Each prompt is saved as a data file in prompts/ (RTF.txt, CO-STAR.txt, CoT.txt) and report.md explains the rationale and expected behaviour for each framework, satisfying both required outputs (prompt data files + report).

## Task 2
- Awarded: 1b   (max 1b)
- Commentary: The Task 1 prompts were used to generate predictions, stored per prompt (data/RTF, data/CO-STAR, data/CoT) with model/prompt/time/score metadata in runs.csv. The report compares accuracy (94.84% RTF, 99.35% CO-STAR, 99.35% CoT) and inference times, and includes a visualization (accuracy.png; not viewable here but described consistently with the text and runs.csv). All required outputs (predictions with identification metadata + brief report + viz + inference times) are present.

## Task 3
- Awarded: 1b   (max 1b)
- Commentary: An original "Row Overlap F1" metric is proposed, argued, and implemented in row_f1.py, which computes per-question precision/recall/F1 over the Task 2 predictions. The report explains the metric, argues it complements (rather than replaces) exact match, and includes comparison tables/graphs (results.csv, results/summary.csv, results/per_question.csv, row_f1_chart.png) showing RTF (0.9851), CO-STAR (0.9935) and CoT (0.9935). All required outputs (metric source code + report) are present.

## Task 4
- Awarded: 0b   (max 2b)
- Commentary: No deliverable is present for Task 4; the Task_4 directory contains only the assignment description (Task_4.md) and no report, tables, graphs, or statistical-significance analysis, so there is nothing to assess. The task explicitly requests a detailed prompt-comparison analysis with significance testing and interpretation of the prompt/model/coding-agent factors, which was not produced.

