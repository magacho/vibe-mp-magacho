---
name: requirement-refiner
description: >-
  Refine, detail, and pressure-test a demand (user story, feature request, or
  formatted requirement) BEFORE any technical or implementation breakdown, in
  order to surface shadow areas and missing information and decide whether it is
  ready to build. The skill drives the demand through Example Mapping (rules /
  examples / questions / new stories), rewrites rules in unambiguous EARS syntax,
  sweeps for edge cases and unwanted behavior, turns examples into Given-When-Then
  scenarios that double as acceptance criteria and tests, and ends with an
  explicit readiness verdict. Use this skill whenever the user wants to refine,
  detail, mature, clarify, or "find the gaps" in a demand or requirement; mentions
  detalhamento de demanda, refinamento de requisitos, critérios de aceitação,
  cenários, casos de teste, áreas de sombra, Example Mapping, Definition of Ready,
  EARS, INVEST, or Gherkin; or hands over a user story / demand and asks what is
  missing, what the edge cases are, or whether it is ready for development. It
  renders the result to the right output target — a Markdown file, a Jira issue, a
  GitHub issue, or another tracker — and generates visual artifacts (use-case,
  sequence, activity, and state diagrams) as portable diagram-as-code when they aid
  clarity. The focus is entirely on requirements, not on solution design or
  estimation.
---

# Requirement Refiner

## What this is for

A demand handed off for development almost always has shadow areas: things the
author assumed, never thought about, or left vague. Those gaps surface later as
rework, mid-sprint clarification, and the wrong thing built confidently. This
skill closes those gaps *before* technical detailing begins, and — just as
important — decides **when the demand is refined enough to stop**.

Two principles govern everything below:

1. **Refining means hunting for what is missing, not polishing what is there.**
   The output is only as good as the questions it raises.
2. **"Ready" does not mean "fully known."** Demanding 100% certainty is itself a
   failure mode (gold-plating, killing negotiability). Stop when every *blocking*
   unknown is resolved or explicitly decided, and the unknowns that remain are
   safe to settle during the build. The readiness gate below makes this precise.

Work in the language of the demand (if the demand is in Portuguese, produce the
refined output in Portuguese).

## Scope

One demand at a time. If the input is an epic or bundles several independent
capabilities, do not try to refine it whole — detect the sprawl in the readiness
gate and propose a split first, then refine each slice on request.

This skill stops at requirements. Do not propose architecture, technical design,
task breakdown, or estimates unless the user explicitly asks afterward.

---

## The refinement loop

Run these phases in order. Phases 1–3 are where shadow areas are found; the
readiness gate (Phase 6) is where you decide if you found enough.

### Phase 0 — Intake and restate

Read the demand. Restate its core in one sentence: **who** (actor/persona),
**what** (capability), **why** (benefit/outcome). If it is not in user-story
shape, reshape it ("As a `<actor>`, I want `<capability>`, so that `<benefit>`")
but keep the original text too. Note explicitly what is *given* versus what you
are *assuming* — assumptions are the first source of shadow.

### Phase 1 — Map (Example Mapping)

This is the engine. Decompose the demand into four kinds of item:

- **Rules** — the business rules / acceptance criteria implied by the demand.
  These are the agreed constraints on scope. Aim for a handful; if you blow past
  ~5–7, that is a sprawl signal for the gate.
- **Examples** — for **each** rule, at least one concrete example with real
  values ("the one where the cart total is exactly R$0,00"). Concrete examples
  expose disagreements that abstract rules hide.
- **Questions** — anything no one in the conversation can answer yet, or any
  assumption you are making to keep moving. Tag every question **BLOCKING** or
  **DEFERRABLE** (see the gate for the test). Questions are the whole point —
  capture them aggressively; a question you almost didn't write down is usually
  the real gap.
- **New stories** — anything that is really a separate increment of value. Slice
  it out and set it aside.

### Phase 2 — Sharpen (EARS + ambiguity hunt)

Rewrite each rule as an unambiguous requirement using **EARS** syntax (see
`references/ears.md` for the five patterns and how to choose). EARS forces you to
name the trigger, the precondition/state, and the exact system response, which is
where vagueness hides.

While rewriting, hunt vague terms — *fast, intuitive, secure, simple, several,
appropriate, etc.* Each one is either quantified ("within 1 second", "at least 3
characters") or, if you can't quantify it, raised as a **BLOCKING** question.
Vague-but-unquantified acceptance criteria are untestable and must not pass the
gate.

Add the **negative** requirements — what the system must *not* do — using the
unwanted-behavior pattern. These are routinely forgotten and are pure shadow.

### Phase 3 — Edge sweep

Most missing information lives in cases the author never pictured. Walk the demand
through the edge-case checklist in `references/edge-cases.md`, category by
category (empty/invalid input, boundaries, concurrency, permissions, state, errors
and failures, scale, etc.). Each case you uncover becomes a new example, a new
rule, or a new question. Do not skip this phase — it is the highest-yield step for
reducing shadow.

### Phase 4 — Scenarios and tests

Turn the examples into **Given-When-Then** scenarios (Gherkin). See
`references/scenarios.md`. Each scenario simultaneously serves as an acceptance
criterion and a definition of an acceptance test. Label each as happy-path, edge,
or error, and make sure every rule from phase 2 has at least one scenario and the
error/edge scenarios from phase 3 are represented.

### Phase 5 — Visualize (diagrams)

Whenever a picture removes ambiguity faster than prose, generate one or more
diagrams. They are first-class deliverables, not decoration: a **use-case** diagram
pins down scope and actors, a **sequence** diagram makes an event flow unambiguous
(it maps directly onto the WHEN rules and Given-When-Then steps), an
**activity/flowchart** exposes the decision branches — including the error paths
found in Phase 3 — and a **state** diagram captures the lifecycle behind the WHILE
rules.

Generate diagrams as portable, editable **diagram-as-code** and **match the
project's existing convention**: if the project uses PlantUML, emit PlantUML; if it
uses Mermaid, emit Mermaid. Default to Mermaid for portability (it renders directly
in GitHub and most Markdown viewers) and use PlantUML when true UML notation or a
native use-case diagram is needed. Generate only the diagrams that earn their place
for this demand — don't produce all of them by reflex. See `references/diagrams.md`.

### Phase 6 — Readiness gate

Apply the gate below and assign exactly one verdict. This is the part that decides
"enough or keep going."

### Phase 7 — Render to the target

The phases above produce *content*; this phase renders it to wherever the demand
will live. Keep content and rendering separate — the same refined demand can be
emitted as a Markdown file, a Jira issue, or a GitHub issue without changing its
substance. Detect or ask for the target, then follow `references/output-targets.md`
for that target's conventions, laying the document out per
`references/output-template.md` and embedding the Phase 5 diagrams in whatever form
the target renders.

---

## The readiness gate (stopping criterion)

Classify the demand into exactly one of three verdicts. The map's "shape" gives
the first signal; the checklist confirms it.

### Verdict A — NOT READY (refine more)

Any one of these is enough to land here:

- There is **≥1 BLOCKING open question**.
- A rule still contains a vague term that changes behavior and wasn't quantified.
- A core scenario has an unknown expected outcome (nobody knows the right result).
- Map shape: a pile of red cards (open questions) relative to rules/examples.

→ Output the demand refined *so far* plus a **numbered list of the blocking
questions** that must be answered before it can proceed. Where this skill runs in
a conversation, ask those questions back to the user (batched, numbered), then
re-enter the loop with their answers. Do **not** dress an unanswered demand up as
finished.

### Verdict B — TOO BIG / SPLIT

Land here if:

- There are more than ~5–7 rules, or
- The demand contains multiple independent capabilities, or
- Examples sprawl across unrelated user journeys.

→ Propose a split into N smaller demands, each independently valuable and small
(INVEST "I" and "S"). Offer to refine each slice. A demand that is too big can't
be meaningfully judged "ready," so resolve size before readiness.

### Verdict C — READY

All of the following hold:

- **Zero blocking questions** remain — each is either answered, or explicitly
  decided with the assumption recorded.
- Every rule is in clean EARS form and is **objectively testable** (no vague,
  unquantified terms).
- Happy path **and** the key error/edge cases each have a Given-When-Then scenario.
- INVEST holds (Independent, Negotiable, Valuable, Estimable, Small, Testable).
- The only questions left are **DEFERRABLE**.

→ Output the full refined package and state plainly that it is ready, listing any
**recorded assumptions** and any **deferred questions** so nothing is silently
swept under the rug.

### The BLOCKING vs DEFERRABLE test

This single distinction is the heart of "enough or more."

- A question is **BLOCKING** if getting the answer wrong would cause rework or
  build the wrong thing — i.e., reasonable people would build materially
  different things depending on the answer.
- A question is **DEFERRABLE** if any reasonable choice is acceptable and changing
  it later is cheap. These can be settled during the build; record them, don't
  block on them.

When unsure, treat it as blocking — but state why, so the user can overrule.

---

## Reference files

- `references/ears.md` — the five EARS patterns, the general clause order, worked
  conversions from vague prose to EARS. Read during Phase 2.
- `references/edge-cases.md` — the systematic edge-case / unwanted-behavior
  checklist, organized by category. Read during Phase 3.
- `references/scenarios.md` — how to write Given-When-Then scenarios that double
  as acceptance criteria and tests, including data tables and scenario outlines.
  Read during Phase 4.
- `references/diagrams.md` — which diagram fits which artifact, and portable
  Mermaid / PlantUML snippets that adapt to the project's convention. Read during
  Phase 5.
- `references/output-template.md` — the canonical structure of the refined-demand
  document. Read during Phase 7.
- `references/output-targets.md` — how to render that structure into a Markdown
  file, a Jira issue, a GitHub issue, or a generic tracker. Read during Phase 7.

## Operating notes

- **The output adapts to where the demand lives.** Don't assume Markdown. Detect
  or ask the target: a `.md` file for repos/wikis, a Jira issue, a GitHub issue, or
  another tracker — and render to that target's conventions
  (`references/output-targets.md`). When an issue-tracker connector is available
  (e.g. Atlassian/GitHub), offer to create the issue directly; otherwise produce a
  clean ready-to-paste document. If the user wants a formal `.docx` hand-off,
  produce it with the docx skill afterward.
- **Prefer visual artifacts when they clarify.** Generate diagrams (use-case,
  sequence, activity, state, …) as diagram-as-code in the project's convention so
  they drop straight into the chosen target.
- Be conversational about the blocking questions — the fastest path to READY is
  usually to ask the user the 2–5 things that actually block, rather than guessing
  and recording five shaky assumptions.
- Keep the focus on *requirements*. The moment you find yourself describing *how*
  to implement, stop and convert that into a rule about *what* the outcome must be.
