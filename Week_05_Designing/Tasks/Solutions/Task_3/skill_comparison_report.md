# Task 3: Comparison report, with and without skills

**Course:** Software Engineering using AI · **Author:** Erik Kammer · **Date:** 29 October 2026
**System:** Not Far(m) From Home (NFFH), used for both runs
**Skills compared:** `architecture-exploration` and `architecture-decision-record`

## 1. What was compared

| | Without skills (Tasks 1 + 2) | With skills (Task 3 re-run) |
|---|---|---|
| Source transcripts | `Task_1/NFFH_conversation.pdf`, `Task_2/NFFH_ADR_conversation.pdf` | `Task_3/NFFH_conversation_export.pdf` |
| Project | NFFH | NFFH (same project) |
| Scope given | Small region, few hundred clients, team of 3, ~3 months, low budget, web only | Same |

Both runs used the same project and scope, so differences come from the skills and from how much of the process I ran. They don't come from the requirements.

## 2. Results

| Metric | Without skills | With skills |
|---|---|---|
| Time (approx.) | ~85 min (Task 1 ~50 min, Task 2 ~35 min), plus ~30 min drafting the kickoff prompt beforehand | ~10 min |
| My prompts | 12 (Task 1: 9, Task 2: 3) | 2 |
| Kickoff prompt | Hand-written, with role, notes rule, assumptions and "stop after overview"; needed several rewrites | One line: "Use the architecture-exploration skill on NFFH.txt" + scope |
| Notes file kept automatically | Yes, because I asked in the first prompt | Yes, from the skill, without being asked |
| Requirements analysis and open issues | 12 open issues, built up over the conversation | 16 open issues in the first reply, data-model-changing ones first |
| Scope questions asked by the assistant | No; I had to supply and defend the scope myself | Yes; it asked for stack experience, grading criteria and compliance |
| Architectures proposed | 3 (monolith, microservices, BaaS) | Same 3, with a flowchart plan for each deep dive |
| Deep dives, comparison table, scope-based choice | Done (6 exchanges + 3 follow-up Q&As) | **Skipped** (I went straight to the ADR) |
| ADR revision rounds to reach the final structure | 3 (draft, then table, then diagram + TL;DR + shorter pros/cons) | 1 (first draft) |
| First ADR draft had TL;DR, options-vs-drivers table, diagram | No, all added on request | Yes, all three |
| Risks with mitigations *and* verifying tests | Mitigations only | Mitigations and tests (7 risks) |
| ADR change log with "why I asked / what changed" | Yes | Yes, same format |
| Final ADR status | Proposed | Proposed |

## 3. Observations

**What the skills clearly improved**
- **No prompt engineering needed.** The structure I spent time crafting before Task 1 (role, standing notes rule, scope, overview-then-stop) is now built into the skill. The kickoff shrank to one line.
- **The ADR came out right on the first draft.** Everything I added by hand in Task 2 (TL;DR, comparison table, diagram) was there in the first version, so the three revision rounds weren't needed.
- **Lessons from Task 1 carried over.** The new ADR already contains points I only reached through follow-up questions in Task 1: the conditional `UPDATE … WHERE qty >= :n` for overselling, a `CHECK` constraint as a safety net, and the "fails closed vs. fails open" security argument stated with a condition attached. The skill turned my questions into its default checklist.
- **Better requirements handling.** More open issues, ordered by impact, plus the assistant asking for missing scope instead of assuming it.
- **The assistant was transparent.** When I skipped phases, the ADR skill said so, marked the ADR as Proposed, and flagged every rating and argument it added beyond the notes for me to confirm.

**Caveats (why the speedup is not entirely the skill's credit)**
- **I skipped the deep dives, comparison and scope choice** in the re-run. That means less discussion happened, and the ADR's Strong/Good/Weak ratings rest on first impressions plus the skill's checklist rather than on argued deep dives. A fair estimate is that a full run with the skills would take about 25–35 minutes, still clearly faster than ~85 minutes.
- **Same project both times.** The re-run used NFFH again. That makes the comparison cleaner, but it doesn't show that the skills generalise to a different system, such as RecipeCove or Teamify.
- **Less of my own understanding is visible.** Task 1 was graded on whether I understood the architectures. The fast run produces a good ADR but almost no discussion. The skills save time on structure, not on learning.
- **Times are approximate**, estimated from message timestamps and file save times.

## 4. What the skills still miss / suggested improvements

1. **The ADR skill shouldn't silently proceed on thin notes.** If the deep dives or comparison are missing, it should first offer to run them (or a short version), and only then draft the ADR as "Proposed, unverified".
2. **Carry the scope answers across skills.** The exploration skill asked about stack experience and grading criteria. When those go unanswered, the ADR skill should list them as REQUIRED open issues, which it partly did, and ask again before setting Status to Accepted.
3. **Add a closing step** that resolves the data-model open issues (multi-farm cart, stock timing, no-shows) and sets Status to Accepted once confirmed. Neither run ended with an accepted ADR.
4. **Test on a second project** to confirm nothing NFFH-specific leaked into the skills.

## 5. Conclusion

The skills cut my prompts from 12 to 2 and the time from roughly 85 minutes (plus prompt preparation) to about 10. The ADR reached its final structure in the first draft instead of after three revision rounds. Part of that gain came from skipping the exploration phases, so the realistic saving for a complete run is smaller, though still large: roughly two-thirds of the time. The biggest value is that the structure and the lessons from Tasks 1 and 2 are reusable without rewriting the prompts. The main limit is that the skills make it easy to skip the discussion that builds real understanding, which was the point of Task 1.
