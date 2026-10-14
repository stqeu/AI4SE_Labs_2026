# Task 3 Report

## The metric: Row Overlap F1
The Task 2 metric only checks if a query returns exactly the right rows, so it is all or nothing. Row Overlap F1 instead checks how many of the returned rows are correct and how many of the correct rows were found, and combines both into one score between 0 and 1. The final score of a prompt is the average over all questions.

## Why it is a good metric
A query that returns 63 rows instead of 62 is almost right, but exact match gives it 0, the same as a completely wrong query. Row Overlap F1 gives partial credit, so it shows how close the wrong answers were. It fits this problem because every query returns rows that can be compared with the expected ones.

## Complement or replacement?
It complements the original metric rather than replacing it. Exact match still says whether the answer is fully correct, and Row Overlap F1 shows how bad the mistakes were.

## Implementation
`row_f1.py` runs the predictions from Task 2 and saves the scores to `results.csv`.

## Results
| Prompt | Accuracy (Task 2) | Row Overlap F1 |
|---|---|---|
| RTF | 94.84 % | 98.51 % |
| CO-STAR | 99.35 % | 99.35 % |
| CoT | 99.35 % | 99.35 % |

## Comparison
- **RTF** improves the most, because most of its mistakes were small (a few extra rows).
- **CO-STAR and CoT** stay the same, because their only mistake (question 66) returned no rows at all.
- CO-STAR and CoT are still the best, but the gap to RTF is much smaller than with exact match.
