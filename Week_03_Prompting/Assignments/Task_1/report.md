# Task 1 Report

All three frameworks were taken from https://frompting.com/frameworks. The prompts are in `prompts/` (`RTF.txt`, `CO-STAR.txt`, `CoT.txt`).

## RTF (Role, Task, Format)
A short prompt with only a role, a task and an output format, chosen as a simple baseline. I expect mostly correct queries, but some mistakes since it gives no extra context.

## CO-STAR (Context, Objective, Style, Tone, Audience, Response)
Chosen because text-to-SQL needs a lot of context (schema, table links, output format), and CO-STAR has a section for each. I expect higher accuracy than RTF.

## CoT (Chain of Thought)
Chosen because some questions are tricky, and reasoning step by step should help with them. I expect accuracy similar to CO-STAR, but a longer inference time.
