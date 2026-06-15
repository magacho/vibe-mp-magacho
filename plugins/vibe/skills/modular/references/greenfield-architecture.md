# Mode B — Architecting a new project

You are designing module boundaries before (or alongside) the first code. Same end goal as Mode A: a structure where each future change touches one module, so each change loads only that module into context. Read the shared foundation in `SKILL.md` first; this file is the step-by-step for the greenfield case.

## The one rule that matters most (and it's the opposite of Mode A)

In a refactor the danger is rewriting too much. Here the danger is **designing too much**. The prime directive is: **match the structure to what the project actually needs to do now, and leave room to evolve.** Premature abstraction — interfaces with one implementation, layers nothing crosses, "flexibility" for requirements that may never arrive — produces *more* coupling and *more* context to hold, not less. It is the most common way a from-scratch architecture fails the very goal it was built for.

So the architect's discipline is restraint: design the boundaries you can justify from real, known requirements, and stop. A module you can merge later is cheap; an abstraction everything already depends on is expensive to remove. When unsure between a simpler and a more elaborate structure, choose the simpler one and let real need pull it apart later.

## Workflow

### 1. Understand the domain and the real requirements

You cannot draw good boundaries without knowing what the system does. Before proposing any structure, get from the user:

- The core capabilities the system must deliver (the verbs: "authenticate users", "process payments", "generate reports").
- What's genuinely known now versus speculative. Design for the known; note the speculative without building for it.
- Hard constraints: existing systems to integrate with, the stack, team shape, performance or compliance needs that force a boundary.

Don't design in a vacuum — ask. This is the architect's most important input and the source has none of it.

### 2. Derive modules from responsibilities

Turn the capabilities into modules, each owning one responsibility, using the "good module" principles in `SKILL.md`. A useful test: each module should map to something a person on the team would name as "the X part of the system." If a proposed module is just a technical bucket with no clear owner-concept ("helpers", "managers", "core"), it's probably not a real boundary.

Resist splitting finer than the requirements justify. Three honest modules beat ten speculative ones.

### 3. Define dependency direction up front

This is the architect's highest-leverage move and the thing a refactor has to fight to recover later. Decide, before code exists, the allowed direction of dependencies — typically as layers, e.g. `domain ← application ← infrastructure ← interface`, where each may depend only on the ones to its left. Write the rule down and, where the language allows, make it *enforceable* (see `references/dependency-tools.md` for contract/boundary linters). A cycle that's impossible to introduce never has to be untangled.

### 4. Design the public contracts before the internals

Define what each module *exposes* — its API, its types, its entry points — before writing what's inside. Other modules depend on these contracts, never on internals. This is what keeps coupling low: a module can be rebuilt entirely as long as its contract holds, and a change inside it loads only it into context. Keep each contract as small as the consumers actually require.

### 5. Present the architecture, impacts, and risks — then discuss

Same hard checkpoint as Mode A, tuned for design. Architecture decisions are *expensive to reverse*, so this conversation matters even more — it's cheaper to change a diagram than a codebase built on it. Present:

- **The proposed module map** — each module, its one-sentence responsibility, and the dependency-direction rule between them. A diagram or simple layered list.
- **The contracts** — the public surface of each module, since that's what everything else will commit to.
- **The tradeoffs** — what this structure makes easy and what it makes harder. Every boundary has a cost on the path that has to cross it; name them.
- **The risks, honestly** — chiefly: am I over-structuring for imagined needs? Is a boundary likely to be in the wrong place given how little is known yet? Is there a simpler structure that meets the known requirements? Flag where you're designing on assumption rather than fact.

Then **discuss** — invite the user to challenge boundaries and especially to cut speculative ones. Adjust and show the revised map before any skeleton is built. For larger systems, agree to skeleton one slice end-to-end first, confirm the shape feels right in practice, then continue.

### 6. Build the skeleton and lock in the rules

Once agreed, create the module skeleton: the folder/file layout, each module's public interface as the stable entry point, and the dependency rules captured as enforceable config where possible. New code then falls into the right module by default. Finish by persisting the rules so future work stays inside the lines (`references/environment-setup.md`) — a fresh architecture decays fastest, because there's no existing structure resisting drift.

## The throughline

Low coupling isn't the goal; it's the means. The goal is that six months from now, a change to how reports are generated means opening the reporting module and nothing else. Every design decision should be checked against that: does this boundary let someone work on one thing while ignoring the rest? If yes, keep it. If it's there for elegance or imagined futures, cut it.
