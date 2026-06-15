# Detecting coupling and circular dependencies by language

Use these to verify module boundaries mechanically instead of by eye. Run the relevant one after a split to confirm you didn't introduce a cycle. Commands change over time and across project setups — confirm the tool is installed and check its current usage before relying on it.

## JavaScript / TypeScript

- **madge** — visualizes the dependency graph and flags circular imports.
  - Find cycles: `npx madge --circular src/`
  - Generate a graph image: `npx madge --image graph.svg src/`
- **dependency-cruiser** — lets you define and enforce boundary rules (e.g. "nothing in `utils/` may import from `features/`") as a config the build can check.￼
- **eslint-plugin-import** — the `import/no-cycle` rule fails the lint on circular imports during normal development.

## Python

- **pydeps** — draws the import graph: `pydeps yourpackage --max-bacon=2`
- **import-linter** — define layered "contracts" (e.g. domain may not import infrastructure) and enforce them in CI.
- Quick manual check: circular imports in Python often surface as `ImportError`/`partially initialized module` at runtime — a failing import is itself a signal.

## Java / Kotlin

- **jdeps** (ships with the JDK) — `jdeps -verbose:class yourapp.jar` shows class-level dependencies; look for back-edges between packages.
- **ArchUnit** — write tests that assert architectural rules (layer access, no cycles between packages) and run them with the normal test suite.

## Go

- `go mod graph` for module-level edges.
- **go-cleanarch** or similar linters to enforce layer boundaries.

## Language-agnostic fallback

If no tool is set up, you can still reason about cycles structurally: for each module, list its imports; trace whether following those imports ever leads back to the starting module. Any path that returns to its origin is a cycle to break — usually by extracting the shared piece both ends depend on into a new lower-level module.

The mechanical check matters because "I think the dependencies look fine" is exactly the kind of judgment that misses a three-hop cycle. Prefer a tool that fails loudly.
