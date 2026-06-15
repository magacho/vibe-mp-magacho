# Persisting module rules across environments

The goal: after a clean split, capture the project's module rules so future sessions respect them automatically. Where these rules live depends on where the user works.

## Claude Code (terminal / repo)

Claude Code reads a layered set of instruction files. Use the layers so high-priority rules don't get buried:

- **`./CLAUDE.md`** (repo root) — core architecture rules for this project: the list of modules, each one's responsibility, and the allowed direction of imports. Keep it tight — a bloated file dilutes its own instructions. Bullet points, not paragraphs. Lead with prohibitions (what must not import what).
- **`.claude/rules/*.md`** — path-scoped rules that only load when Claude touches matching files. Use YAML frontmatter to target a module, e.g. a rule that only applies under `src/api/**` so API constraints don't clutter context while editing UI code.
- **Optional `/modularize` and `/review` slash commands** in `.claude/commands/` — reusable command files that run the extraction or boundary-check workflow on demand, so the user doesn't retype the process each time.

These are Claude Code-specific mechanics; they don't carry over to Claude.ai.

## Claude.ai (chat interface)

There's no repo-level instruction file here. Two durable options:

- **A Project** (if the user has Claude Pro/Team/Enterprise): put the module map and import rules in the Project's custom instructions or as a Project knowledge file. Every chat in that Project then inherits them.
- **This very skill**: the module rules *are* portable expertise. Once the project's boundaries stabilize, fold a short "project module map" section into a project-specific copy of this skill so it travels with the user.

## Both

Whatever the surface, the content of the rules is the same and is the valuable part:

1. The list of modules and the one-sentence responsibility of each.
2. The allowed import directions (a simple "X may import Y, never the reverse" table).
3. The public surface of each module — what it exports — so new code depends only on the intended entry points.

Keep this list short and current. A rules file that's drifted out of date is worse than none, because it teaches the wrong boundaries.
