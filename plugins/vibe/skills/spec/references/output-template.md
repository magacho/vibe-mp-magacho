# Output template — refined demand document

Produce the refined demand in this structure, then render it to the chosen target
(see `output-targets.md`) — the structure is the same; only formatting and field
mapping change. Use the demand's language. Keep it tight: every section earns its
place by reducing ambiguity. Omit a section only if it is genuinely empty, and say
so rather than padding.

```markdown
# <Demand title>

## 1. Summary
As a <actor>, I want <capability>, so that <benefit>.
<One short paragraph of context: what problem this solves and for whom.>

## 2. Goal & value
- Problem being solved:
- Primary outcome / success looks like:

## 3. Scope
**In scope:** <bullet list of what this demand covers>
**Out of scope (non-goals):** <what this explicitly does NOT do>

## 4. Assumptions
<Decisions made to move forward, each one a thing someone could later dispute.
If empty, write "None recorded.">

## 5. Business rules (EARS)
A numbered list. Each rule in EARS form, testable, no vague terms.
1. When ..., the system shall ...
2. If ..., then the system shall ...
3. While ..., the system shall ...
...

## 6. Scenarios (acceptance criteria & tests)
Given/When/Then for happy path, edge, and error cases. Label each.
- **[Happy]** Scenario: ...
- **[Edge]** Scenario: ...
- **[Error]** Scenario: ...

## 7. Diagrams
Diagram-as-code (Mermaid or PlantUML, matching the project's convention). Include
only those that clarify this demand — e.g. a use-case for scope/actors, a sequence
for the main flow, an activity diagram for the error branches. Omit if none help.

## 8. Open questions
Numbered. Tag each [BLOCKING] or [DEFERRABLE], and for blocking ones say briefly
why it would change what gets built.
1. [BLOCKING] ... — why it blocks: ...
2. [DEFERRABLE] ...

## 9. Sliced-out stories
Anything that was spun off as a separate increment (with a one-line rationale).
If none, omit.

## 10. Readiness verdict
One of: **READY** / **NOT READY** / **TOO BIG — SPLIT**.
- If READY: confirm zero blocking questions, list recorded assumptions and any
  deferred questions.
- If NOT READY: restate the blocking questions that must be answered next.
- If TOO BIG: present the proposed split and offer to refine each slice.
```

## Notes
- Lead the verdict with the headline word so a skimming reader sees it instantly.
- The open-questions list is the most valuable part of a NOT-READY document — make
  it specific and answerable, not "needs more detail."
- When READY, the scenarios in section 6 should be complete enough to hand
  straight to whoever writes the tests.
- Map every section to the target's fields per `output-targets.md`; never drop the
  verdict or the open questions in translation.
