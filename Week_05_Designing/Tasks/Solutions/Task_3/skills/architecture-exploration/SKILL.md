---
name: architecture-exploration
description: Explore and choose an architecture for a system from a requirements file: 3 options, deep dives, comparison, scope-based choice, with a running notes file.
---

# Architecture exploration

Use when the user attaches a requirements / user-story file and wants to understand and compare architectures before choosing one. Often a learning context (course, report): explanation and trade-off reasoning matter more than a bare verdict. Act as a senior software architect unless told otherwise.

Run the phases below in order. Do not run several phases in one reply unless the user asks; each phase ends with a short hand-back ("pick the next one" / "ask away").

## Standing rule: notes file (applies to EVERY reply, without being asked)

- On the first reply create `notes.txt` (or the name the user gives). After every later reply, update it and send it again.
- Organise by topic, not as a chat log. Keep this section order, numbered in the order they appear in the file:
  0. System summary
  1. Candidate architectures (overview)
  2..n. One deep-dive section per architecture
  then Comparison table, Choosing for the scope, one section per follow-up Q&A,
  and LAST: Open issues / to discuss later (always the final section; never insert a new section after it).
- Section header format: `N. TITLE (exchange #k)`, then `Q (me): <user's question in one line>`, then terse bullets: what was proposed, key trade-offs, contrasts with other options, verdict. Code/SQL snippets allowed.
- Every reply: add new open issues, mark resolved ones, and note decisions that became required.
- If the file is re-attached or read-only, copy it into the working folder and keep going; mention this once.
- End EVERY reply with one line: `📝 notes.txt: <what was added/changed>`.

## Phase 1: Read the requirements (first reply)

1. Summarise the system in 3-5 bullets, including implicit facts (e.g. what is NOT in scope, and what that means for terms like "order").
2. List the roles. Group the user stories into 4-6 capability groups with their story numbers. Reuse this mapping later.
3. List ambiguities as open issues. Put first the ones that change the data model or the architecture (consistency semantics, multi-entity transactions, session strategy, undefined business terms, missing data such as opening hours or locations).
4. Ask for the scope assumptions in ONE compact block, unless they are already given. Do not block the overview on them, but they are needed before Phase 5:
   - size (users, entities, traffic, regions)
   - team (size, experience, known stacks / frameworks)
   - timeline, hosting budget, platforms (web / mobile)
   - goal of the work (graded on design and testing? on a polished product?)
   - compliance or data location constraints

## Phase 2: Overview of 3 architectures (same first reply)

- Pick 3 options from genuinely different families. State the axis they differ on (e.g. "how the backend is split and who runs it").
- Default trio: layered modular monolith / microservices with API gateway / serverless-BaaS. Swap one if the requirements point elsewhere (event-driven, offline-first, data pipeline, plugin-based).
- For each: 2-3 sentences plus a small ASCII diagram, and one first impression.
- STOP. Ask which one to deep-dive first.

## Phase 3: Deep dive, one architecture per reply

Use this fixed template. Put the flowchart FIRST without being asked.

1. **Flowchart of the key request.** Use the SAME request for all three architectures. Pick the one that touches auth, validation, business rules and data consistency at once (checkout, booking, submission). Show the error exits with status codes (401/403, 400, 409...). Render it as an inline visual. If boxes mean different things (managed vs code you write, service vs event), add a colour legend. In the 2nd and 3rd dives, open with 2-3 sentences comparing against the earlier flowcharts.
2. **How it's organised:** the modules or services mapped to story numbers (a table is fine here), the layers, a stack example, and the one "golden rule" that keeps the structure clean.
3. **Benefits**
4. **Trade-offs**
5. **Difficult parts (design level),** numbered. Always check: authorisation by ownership (not just role), boundaries, operations spanning several entities, deleting referenced data, and admin/reporting queries.
6. **Painful low-level details,** each with a concrete fix (SQL or code snippet). Always check the same list for every architecture so the comparison is fair:
   - concurrency races on shared counters or stock
   - money and number types, units
   - dates and timezones
   - sessions / tokens and revocation; CSRF / XSS exposure
   - duplicate or out-of-order messages, idempotency
   - secrets and keys
   - scheduled or cleanup jobs
   - external integrations (maps, email, payments)
   - caching hot queries
   - environment drift, testing approach, data location
7. **Verdict** in 1-2 sentences, plus a one-line teaser for the next architecture.

## Phase 4: Comparison table

- Columns = the 3 options. Rows:
  1. implementation benefits
  2. running benefits
  3. implementation drawbacks
  4. running drawbacks
- Keep points brief; the deep dives hold the detail.
- End with a one-line summary per option.

## Phase 5: Choose for the given scope

- If the user proposes a choice, answer "Mostly yes / No" in the first sentence, then correct any part of the assumption that is inaccurate.
- Cover, in this order:
  1. why the clearly wrong option is out (tie its costs to the constraints)
  2. why the winner wins
  3. where the runner-up beats the winner on these constraints
  4. caveats (e.g. free-tier limits)
  5. what would flip the decision
  6. a middle path if one exists (e.g. "rent the boring parts": managed DB and host plus the framework's security module)
- End with: chosen / runner-up / rejected.
- Report tip: argue "X fits OUR constraints, and here is what would make us pick Y", not "X is best".

## Phase 6: Follow-up Q&A

- Ground every answer in the requirements, using named actors, concrete data and story numbers.
- For mechanism questions, show:
  - the unsafe version and a timeline of how it fails
  - "fixes" that don't work, and why
  - the safe version
  - alternatives
  - how to test it (integration test, not unit test)
- For "is X safer / better" claims:
  - judge by what happens when an inexperienced team makes mistakes (failure mode: closed vs open; attack surface; reviewability; testability; familiarity)
  - say where the claim breaks and attach the condition under which it holds
  - give report-ready wording as "Avoid: ... / Better: ...", structured as claim + reasons + condition + acknowledgement of the alternative's strength
- Each Q&A becomes its own notes section. Add any new required condition to the open issues.

## Handoff

Once an architecture is chosen, offer to write an ADR (architecture-decision-record skill), using notes.txt as the source material.
