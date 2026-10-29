---
name: architecture-decision-record
description: Write and revise an Architecture Decision Record from exploration notes, in a fixed structure with TL;DR, drivers table, diagram, binding rules, and a change log.
---

# Architecture Decision Record (ADR)

Use when the user wants a formal ADR choosing an architecture. The input is usually exploration notes (e.g. from the architecture-exploration skill) plus the requirements file. Output:
- ONE ADR document, as an editable document artifact when the session offers one, otherwise a Markdown file
- a change-log file

## Standing rule: change log (EVERY reply, without being asked)

- Keep `<task>_notes.txt` (default `adr_log.txt`, or the name given). Append one entry per reply, then send the file:

```
UPDATE #n - YYYY-MM-DD - <short title>
-------------------------------------
Why I asked for it:
- <the user's reason, first person, in their own terms>

What changed in the ADR:
- <section: change>, per section touched; for a new version give a section-by-section outline

Decisions/assumptions I made while drafting (please confirm):
- <only if any>

Questions for review:
k. <numbered continuously across ALL updates>
```

- End EVERY reply with one line: `📝 <logfile>: <what was added>`.

## Process

1. Read the notes and requirements fully. List every argument, rule and open issue you will use. Add no new arguments beyond the notes; if one is unavoidable, flag it in the log.
2. If the user says "no tables/diagrams yet", respect it: write the text sections and note in the log what is held back. Otherwise produce the FULL structure below in the first draft. Users otherwise end up asking separately for the table ("hard to tell why X won"), the TL;DR, shorter pros/cons and the diagram.
3. Create the document with headings first, then fill it section by section.
4. Verify: every table rating traces to the notes; drivers appear in the same order everywhere; the TL;DR, the Decision section and the table verdict agree.
5. Write the log entry. Ask the standard review questions (below) that are still open.

## Final structure

**Title:** `ADR-NNN: Architecture for <System>`. **Byline:** date · deciders.

**TL;DR** (3-4 sentences):
- the chosen option in one phrase
- its 3 strongest reasons
- the runner-up
- the rejected option, with a 2-word reason

**Status:**
- status (Proposed, pending team review / Accepted / Superseded) plus a one-line restatement of the decision
- Deciders
- Format (Nygard-style, extended with MADR decision drivers and considered options)
- Supersedes / Superseded by
- Source material

**Context:**
- the system in 2-3 sentences, with implicit facts
- roles, and capability groups with story numbers
- scope and constraints (size, team, time, budget, platform, goal of the work)
- technical forces: bullets naming the hard requirements that discriminate between the options (consistency, ownership-based authorisation, safe deletes, revocable sessions, team experience)

**Decision drivers:** 5-7 items, numbered in priority order for THIS scope, each written as `Name: one-line test`. Typical drivers: deliverability, security under inexperience (fail closed), data consistency, cost / operations load, visible and testable design, evolvability / lock-in.

**Considered options:** for each option:
- a 2-3 sentence description
- `Good:` one line with 2-3 points
- `Bad:` one line with 2-3 points

Keep long arguments out of this section; they live in Rationale, Consequences and the table.

**Options against the decision drivers** (subsection at the end of Considered options):
- a lead sentence stating the takeaway (e.g. "X is the only option with no Weak rating on the top three drivers")
- a table: rows = the drivers in priority order plus a Verdict row; columns = the options
- each cell = `Strong / Good / Weak: short reason`
- Verdict row: Chosen / Runner-up / Rejected

**Decision:**
1. One sentence: "We will build <system> as <option>, and rent the commodity parts (...). Option Y is the documented runner-up; Option Z is rejected."
2. Diagram right after that sentence, as a component/layer view of the chosen architecture:
   - clients
   - the protocol / session mechanism on the entry arrow
   - the deployable unit
   - the security layer, highlighted when the rationale depends on it
   - modules × layers
   - the ONE cross-module call that illustrates the boundary rule
   - the data store, with its key constraints
   - external services as dashed boxes

   Add a caption and one reading sentence under it. Mark it tentative in the log until the user confirms.
3. **Binding rules that come with this decision**, numbered 6-10, concrete and testable. Cover:
   - modules and boundary enforcement
   - layers and their responsibilities
   - authentication (framework module, no hand-rolled crypto)
   - sessions and revocation
   - authorisation (role AND ownership, where it is checked)
   - the consistency mechanism (exact statement or pattern, plus a DB constraint as safety net)
   - data rules (money type, snapshots, date types, delete policy)
   - external integrations

**Rationale:**
- open with "<option> best fits our constraints, not the best architecture in general"
- *Why not <rejected>*: its benefits have no value at this scope, and its costs land on our constraints
- *Why <chosen> over <runner-up>*: bold lead-ins per driver; for security, use the precise wording: claim + reasons + condition + acknowledgement of the alternative's strength
- *What <runner-up> does better, and why we accept the loss*: how the middle path closes the gap

**Consequences:**
- Positive
- Negative
- Risks and mitigations, each as "risk: mitigation; verified by <test>". Include a schedule risk: build the rule-heavy core first and repetitive CRUD last.

**Conditions to revisit:**
- switch to the runner-up if...
- move toward the rejected option only if... (and how the split would follow existing boundaries)
- revisit the key claim if its condition cannot be met

**Open issues and follow-up decisions:** a ☐ checklist, introduced with "these do not change the choice, but each needs its own decision". Mark the ones that are REQUIRED for the rationale to hold (e.g. the framework / stack choice).

## Writing rules

- Use the same terms everywhere (option letters, module names, driver names).
- Never write "X is more secure". Write "lower-risk for our team, because ..., on the condition that ...".
- Keep implementation detail at binding-rule level; flag anything deeper as a candidate for a later design doc.
- Edits requested later (shorten, add, move) change only the named sections; log exactly what moved where.

## Standard review questions

Ask the ones still open, numbered in the log:
1. Which backend framework / stack does the team know best? It fills the stack open issue and makes the auth rule concrete.
2. One ADR, or split follow-ups into ADR-002, ADR-003 ...?
3. Is the binding-rule detail level right, or should parts move to a design doc?
4. Strong/Good/Weak ratings, or weighted numeric scores?
5. Diagram: component/layer view, key-request flow, or both?
