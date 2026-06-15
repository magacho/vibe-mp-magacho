# Mode A — Refactoring an existing project

You are untangling code that already works. The prime directive is **preserve behavior**. Read the shared foundation in `SKILL.md` first; this file is the step-by-step for the refactor case.

## The one rule that matters most

When you relocate code from file A to file B, the moved code must be **byte-for-byte identical**: same names, same comments, same formatting, same logic. You are the hands moving the blocks, not the brain reimagining them.

This exists because the default instinct when reorganizing is to *rewrite*. In a battle-tested codebase full of edge cases and thin on tests, a moved function that looks 99% the same can hide a silent regression that costs hours to find. So: **move code, don't regenerate it.**

Structural changes (moving things, reducing coupling) and behavioral changes (renaming, simplifying, "modernizing") must **never happen in the same step**. Move first, verify it's a pure move, commit. Improve later, separately. Mixing them destroys your ability to verify either one.

## Workflow

Follow in order. Don't skip analysis — most bad modularization comes from cutting before understanding.

### 1. Analyze before touching anything

- Read the target file(s) and list the logical groups inside (e.g. in a `utils.js`: string helpers, date helpers, validation, formatting).
- For each group, note what it *imports* (its dependencies) and what *imports it* (its dependents).
- Map the direction dependencies flow and hunt for existing cycles (use `references/dependency-tools.md`).

Surface this analysis to the user — they know things the source doesn't reveal.

### 2. Plan the module boundaries

Apply the "good module" principles from `SKILL.md` to propose a target structure. For each existing dependency cycle you found, plan how to break it — usually by extracting the shared piece into a new lower-level module both sides can depend on. This phase produces a *proposal*, not changes.

### 3. Present the plan, impacts, and risks — then discuss

Hard checkpoint. Do **not** move code until the user has seen and approved the plan. Present, in plain terms:

- **The proposed structure** — new modules, each one's one-sentence responsibility, and which existing code moves into each. A simple before → after of the layout.
- **The blast radius** — which files get touched, concretely: "moves 14 functions out of `utils.js` into 4 new files and updates imports in ~30 call sites." A wide ripple isn't wrong, but the user should know its size first.
- **What the public surface becomes** — what each new module exports, i.e. what the rest of the code may now depend on. This determines future coupling, so it's the part most worth a second opinion.
- **The risks, honestly** — name them: code being moved has no test coverage; a cycle the split exposes and forces a decision on; a module whose responsibility isn't actually clean; a call site that's hard to update mechanically.

Then **discuss** — invite pushback. Does the grouping match how they think about the system? Is a boundary cutting through something that should stay together? Would they rather pilot one module first? Adjust and, if it changed meaningfully, show the revised plan before proceeding. For large plans, do one module as a trial run, validate it together, then continue.

### 4. Extract (move, verbatim)

For each group, lowest-level modules first:

- Cut the code from the source and paste it into its new home, unchanged.
- Add the necessary imports/exports — the *only* code you write from scratch.
- Update every reference to point at the new location.

One module at a time; validate after each before starting the next. Note any "tidy up while I'm here" ideas in a separate list for later — don't act on them now.

### 5. Validate every move

- **Inspect the diff.** Lines *removed* from the source, *added* to the new file, no changes to the logic between. If the diff shows modified lines inside a moved block, you rewrote something — revert and redo as a clean move. (`git diff`, or compare side by side without git.)
- **Run the existing tests.** Green tests after each move are the strongest evidence behavior is unchanged.
- **Re-check dependency direction.** Confirm no new cycle: the new module shouldn't import anything that imports it back.

If the code being moved has no tests, say so plainly — moving untested code is riskier, and a thin characterization test before the move is worth the time.

## Hard prohibitions during extraction

State these to yourself before starting and don't break them mid-task:

- Do **not** rename variables, functions, or parameters.
- Do **not** reformat, re-indent, or "clean up" style.
- Do **not** change logic, even to fix a bug you spot — note it separately and tell the user.
- Do **not** upgrade syntax to a newer style (e.g. callbacks → async/await).
- Do **not** combine a move with a behavioral change in the same commit.

Each prohibition is a way the diff stays verifiable, which is the entire safety mechanism.

## Finish

Capture the new module rules so future work respects them (`references/environment-setup.md`). The decoupling only pays off in reduced context-per-change if the boundaries hold over time.
