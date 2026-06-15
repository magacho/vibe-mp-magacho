---
name: modular
description: Design or refactor codebases into clean, low-coupling modules so that any single change, fix, or new feature only requires loading a small slice of the system into context. Covers two scenarios — (A) refactoring an existing/legacy/human-written project to untangle it, and (B) architecting a brand-new project so it starts modular. Use this skill whenever the user wants to modularize, reduce coupling/dependencies, split a large file, untangle a tangled codebase, review module boundaries, OR plan the architecture of a new project with modularity in mind — even if they don't use the word "modularize". Triggers include "this file is too big", "too much dependency between these parts", "help me organize this code", "design the architecture for a new project", or "teach Claude to work in modules here".
---

# Code Modularization

Make a codebase one where **each change touches one module, so each change only needs that module loaded into context.** That is the north star — for humans navigating the code and for an AI working within a limited context window. Everything below serves it: low coupling, clear boundaries, and dependencies that flow in one direction all exist so that fixing a bug or adding a feature means opening one well-defined box instead of the whole system.

## First: which scenario are you in?

This skill works in two modes. Identify the mode before doing anything else, because the governing risk is opposite in each.

- **Mode A — Refactor an existing project.** There is already working code (often legacy, often without AI, often thinly tested). The prime directive is *preserve behavior*: move code, don't rewrite it. The danger is a silent regression. → Follow `references/refactor-existing.md`.
- **Mode B — Architect a new project.** There is little or no code yet; the user wants to start modular. You act as an architect: design boundaries and contracts up front. The danger is the *opposite* — over-engineering and premature abstraction. → Follow `references/greenfield-architecture.md`.

If it's ambiguous (e.g. "small existing prototype we want to grow"), ask the user which fits, or treat it as a small Mode A followed by Mode B planning for the parts not yet built.

Both modes share the principles, the human checkpoint, and the persistence step below. Read this file, then open the reference for your mode.

## The shared foundation: what makes a good module

Both modes aim for the same kind of module. A good module:

- **Has a single, nameable responsibility.** If you can't describe it in one sentence without "and", it's probably two modules.
- **Has a small public surface.** It exposes only what others genuinely need; everything else stays private. A smaller surface means fewer things other code can depend on, which means less coupling and a smaller context to load when working elsewhere.
- **Depends in one direction.** Lower-level modules (utilities, types, domain) must not import higher-level ones (features, pages, entry points). If two modules need each other, that's a design smell — usually a third, shared module wants to be extracted.
- **Groups things that change together.** Code edited in the same breath belongs together (high cohesion); code that changes for unrelated reasons belongs apart.
- **Never forms a cycle.** A imports B and B imports A — directly or through a chain — is the single biggest cause of a codebase feeling "tangled" and is what forces you to load everything at once. Cycles are the thing to hunt down and break in Mode A, and the thing to make structurally impossible in Mode B.

The connection to the goal is direct: small surface + one-way dependencies + no cycles = you can change one module while reading only it and the few it depends on. That is the context reduction the user is after.

## The shared checkpoint: present before you act

In **both** modes there is a hard rule: **present the plan — structure, impacts, and risks — and have a real discussion with the user before making changes.** This is not a confirmation dialog; it's a conversation. The user knows things the code and the requirements don't show: why a "messy" file is shaped that way, which parts are fragile, what's about to be thrown out anyway, or what the project actually needs to do. Surfacing the plan first lets that knowledge correct it before it does damage instead of after.

What "present" means differs slightly by mode (a refactor presents a blast radius and regression risk; an architecture presents tradeoffs and reversibility risk), and each reference file spells out its version. But the spine is identical: propose, show impacts and risks honestly, invite pushback, adjust, and only proceed once the user is genuinely on board. For large plans, agree on a small pilot — one module — validate it together, then continue.

## The shared payoff: keep future work modular

A one-time cleanup or a tidy initial structure decays unless future work respects the boundaries. In both modes, finish by capturing the project's rules so they persist: the list of modules and each one's responsibility, the allowed import directions, and each module's public surface. Where these rules live depends on the environment — see `references/environment-setup.md` (covers both Claude Code and Claude.ai, since the same rules should travel across both).

## Verifying boundaries mechanically

"I think the dependencies look fine" is exactly the judgment that misses a three-hop cycle. When you know the language, use the concrete tools in `references/dependency-tools.md` to detect coupling and cycles automatically rather than by eye — in both modes (to find cycles in Mode A, to confirm the new structure has none in Mode B).

## A note on the metrics you'll see online

Articles cite dramatic numbers ("50–80% token savings", "40% faster delivery"). Treat those as motivation, not promises — they're uncontrolled anecdotes. The real, defensible payoff is concrete and worth stating plainly: a change that touches one module instead of ten, files that fit in context, and a verifiable history. Sell the user on that, not on a percentage.
