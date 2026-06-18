---
name: 360
description: One umbrella command that audits a codebase across all dimensions at once and produces a single Bemobi-branded HTML presentation. Combines AI/token efficiency (how code organization and artifact size inflate AI context cost and prevent surgical edits), maintenance & dead code, code reuse/duplication, and visual-component reuse — each as a deck section with a problem, context cost, suggestion, evaluated solution options, and risk/impact. Use when the user wants a full report, a "raio-x", a 360 review, an executive codebase audit, or to combine several analyses into one deck. Report-only — never auto-applies changes.
allowed-tools: [Bash, Write, Read, Glob, Agent, TaskCreate, TaskUpdate, TaskGet, TaskList]
keywords: [codebase-360, 360, raio-x, audit, executive-report, full-report, ai, maintenance, reuse, duplication, components, deck, presentation, bemobi]
---

# Codebase 360

A single orchestrating command that runs every analysis lens, merges the findings into one
schema, and renders one **Bemobi-branded HTML deck** (`html-presentation` + `bemobi-brand`
conventions). Report-only — never apply changes unless the user explicitly asks, then hand off
to `scip-verify`.

Built on `scip-query`. If the index is missing/stale, run `scip-query reindex` first
(or the `scip-polyglot-setup` skill if `scip-query` itself is absent).

## Sections (v1)

| # | Section | Lens | Primary commands |
|---|---------|------|------------------|
| 🤖 | **AI / Eficiência de Token** | How org/artifact size inflates AI context cost and blocks surgical edits | `context-cost.sh tokens/edit-cost`, `scip-query rdeps/affected/deep-chains/bottlenecks/outline` |
| 🔧 | **Manutenção & Dead Code** | Architecture smells, hidden policies, dead/bloat | `scip-query health/dead/isolated/stale-abstractions/cycles/drift` |
| ♻️ | **Reuso de Código** | Duplicated functions/files, consolidation seams | `scip-query similar/similar-files/convergence/similar-signatures` |
| 🎨 | **Reuso de Componentes Visuais** | Duplicated React components, under-used `ui/` primitives | `scip-query similar-files <components>`, `hotspots`/`rdeps` on `components/ui/*` |

The AI section explicitly carries the "custo de AI" framing: every finding states how many
tokens an AI must load to change that area, so the reader sees where poor organization makes
AI development expensive and non-surgical.

## Workflow

### 0. Preflight: check tooling, help install what's missing (ALWAYS run first)
```bash
bash "$CLAUDE_SKILL_DIR/scripts/check-tools.sh"
```
Reports each dependency as OK / WARN / MISS with an install hint, and exits 1 if a **required**
tool is missing. Required: `scip-query` (npm i -g scip-query), `python3`, and a working scip
CLI + language indexers (via `scip-query check-deps`). Optional (degrade gracefully): a headless
chrome/chromium for screenshots, and the `bemobi-brand` skill for the logo.

If something is MISSING, help the user install it before continuing — do not push through:
- `scip-query` absent, or `check-deps` reports a missing scip CLI / indexer → invoke the
  **`scip-polyglot-setup`** skill (installs the scip CLI + indexers and builds the index).
- `python3` absent → guide the OS install (`apt-get install -y python3` / `brew install python3`).
- chrome/bemobi-brand absent → only WARN; the deck still renders (screenshot/logo degrade).

Re-run `check-tools.sh` until it prints "ready to run" before moving on.

### 1. Prepare
```bash
export PATH="$HOME/.local/bin:$PATH"
scip-query status || scip-query reindex
scip-query stats          # capture documents/symbols for the title slide
```

### 2. Run the four sections (parallelize with subagents)

Spawn one subagent per section (they are independent). Brief each with: the commands above for
its lens, the shared finding schema (below), and "rank by impact ÷ risk, verify before
suggesting deletion, note framework entrypoints as false positives, return ONLY the section
JSON object". The deterministic token math is shared:

```bash
CC="$CLAUDE_SKILL_DIR/scripts/context-cost.sh"
bash "$CC" tokens                 # file token ranking (AI + visual-reuse sections)
bash "$CC" edit-cost <file>       # tokens to edit a file safely (AI section headline)
```

Section briefs:
- **AI / Token:** biggest files (`tokens`), worst `edit-cost`, high `rdeps`/`affected`
  (non-surgical), `deep-chains`, oversized type/domain files (`outline` symbol counts).
- **Manutenção & Dead Code:** `scip-query health`, `dead --min-loc 5 --skip-barrels`,
  `isolated`, `stale-abstractions`, `cycles`, `drift`.
- **Reuso de Código:** `similar --min-similarity 0.5`, `similar-files`, `similar-signatures`;
  for each strong pair, `convergence <a> <b>` for the consolidation prescription.
- **Reuso de Componentes Visuais:** `similar-files --min-similarity 0.6` restricted to
  `src/components/**`; `hotspots`/`rdeps` on `src/components/ui/*` to find under-used or
  bypassed primitives; large `.tsx` from `tokens`.

### 3. Merge into one findings JSON

Combine the section objects into the document, add `stats` and a `scorecard` (one grade per
section). Rank findings within each section by impact ÷ risk.

```json
{
  "project": "Bemobi Teams", "scope": "Repo (src/)", "date": "YYYY-MM-DD",
  "stats": {"documents": 0, "symbols": 0},
  "scorecard": [
    {"dimension": "AI / Token", "grade": "C", "headline": "1 god type-file infla 163 telas"},
    {"dimension": "Manutenção", "grade": "B", "headline": "14 símbolos mortos, 0 ciclos"},
    {"dimension": "Reuso de Código", "grade": "B", "headline": "N pares similares"},
    {"dimension": "Componentes Visuais", "grade": "C", "headline": "M componentes duplicados"}
  ],
  "sections": [
    {"key": "ai", "title": "AI / Eficiência de Token", "color": "#062EED", "icon": "🤖",
     "summary": "Onde a organização do código encarece o contexto da IA.",
     "findings": [
       {"id": "AI1", "title": "…", "priority": "HIGH|MEDIUM|LOW",
        "problem": "…", "evidence_cmd": "scip-query …",
        "context_cost": "edit-context = N tokens; puxado para K contextos",
        "suggestion": "…",
        "options": [{"kind": "Conservadora", "desc": "…", "saves": "~N tok", "risk": "baixo"},
                    {"kind": "Estrutural", "desc": "…", "saves": "~N tok", "risk": "médio"}],
        "risk_impact": "blast radius R; teste sim/não; reversibilidade …",
        "gain": "~N tokens / closure M→m"}]},
    {"key": "maint", "title": "Manutenção & Dead Code", "color": "#6924E1", "icon": "🔧", "summary": "…", "findings": []},
    {"key": "reuse", "title": "Reuso de Código", "color": "#027BFF", "icon": "♻️", "summary": "…", "findings": []},
    {"key": "ui", "title": "Reuso de Componentes Visuais", "color": "#16A34A", "icon": "🎨", "summary": "…", "findings": []}
  ],
  "not_recommended": ["mudanças tentadoras que custam mais conceitos do que removem"]
}
```

Section colors use the Bemobi palette (`#062EED` blue, `#6924E1` purple, `#027BFF` mid-blue,
`#16A34A` green). `context_cost` is optional per finding (most relevant to the AI/Token and
visual sections).

### 3b. Always include: executive summary, golden rules, prompts, estimates

These are NOT optional — every 360 run renders them in the HTML:

- **`exec_summary`** (top-level, after `stats`) — one consolidated table row per finding, so the
  reader sees complexity at a glance. Each row carries a **golden rule** (`rule`): a simple,
  direct, imperative directive that prevents new code from recreating that problem (CLAUDE.md
  voice). One rule per reported problem. Renders after the scorecard as a 6-column table
  (Ação · Esforço · Impacto na operação · Impacto na change · Ganho · Regra de ouro).
  ```json
  "exec_summary": {
    "title": "O que ganhamos com cada ação",
    "intro": "Operação = comportamento em runtime; Change = blast radius do diff.",
    "rows": [
      {"id": "AI1", "dim": "🤖 AI / Eficiência de Token", "priority": "HIGH",
       "status": "feito (opcional)", "action": "…", "effort": "Baixo|Médio|Alto",
       "ops": "Nenhum|Baixo|Médio", "change": "…", "gain": "…",
       "rule": "Página = orquestradora fina; nunca importe a árvore inteira numa page."}
    ]
  }
  ```
- **Per-option `prompt`** — every solution option (Conservadora / Estrutural) gets a
  copy-pasteable implementation prompt (references `concrete-plan`, the target files, the
  constraint, and the verification: `scip-query diff-gate` / `context-cost.sh edit-cost`).
  Renders as a dark "Prompt p/ implementar" block under each option.
- **Per-finding `estimate`** (optional, best for AI/Token) — projected token-reduction table.
  ```json
  "estimate": {"caption": "tokens = bytes/4; 'depois' projetado.",
    "rows": [{"change": "editar /people", "before": "43.272", "after": "~15.000",
              "saved": "~28.000", "pct": "~65%"}]}
  ```

### 4. Render the deck
```bash
python3 "$CLAUDE_SKILL_DIR/scripts/render-deck.py" \
    reports/codebase-360/YYYY-MM-DD.json \
    reports/codebase-360/YYYY-MM-DD.html
```
Produces: title slide → scorecard → executive summary (with golden-rule column) → per section
(divider + finding slides, each option carrying its prompt) → "não recomendado".
The Bemobi logo is resolved from the installed `bemobi-brand` skill (text fallback if absent).

### 5. (optional) verify visually
```bash
google-chrome --headless --no-sandbox --disable-gpu --window-size=1280,800 \
    --screenshot=/tmp/c360.png reports/codebase-360/YYYY-MM-DD.html
# to screenshot a specific slide N: sed 's/goTo(0);/goTo(N);/' file.html > /tmp/x.html
```

### 6. Offer to add the Golden Rules to the analyzed project's CLAUDE.md (ALWAYS run last)

The golden rules already live in the HTML (step 3b) — that is non-negotiable. This final step
is the ONLY opt-in: after the deck is written, offer to also persist the rules in the analyzed
**project's `CLAUDE.md`** so future code generation follows them.

1. Read the project `CLAUDE.md` (if any) and diff its existing rules/conventions against the
   golden rules just produced. Drop duplicates; surface any doc line the rules contradict.
2. Classify each rule: **valid today** vs **target** (references code that does not exist yet —
   verify with `ls`/`scip-query`). Also surface any stale doc line worth correcting.
3. **Ask with `AskUserQuestion`** whether to apply: e.g. (a) only the valid-today rules + doc
   fixes [recommended], (b) all rules with targets marked "(após implementar)", (c) don't touch
   CLAUDE.md. Apply ONLY on explicit confirmation, as an additive `## Golden Rules` section.

Never edit CLAUDE.md without this confirmation — the report itself stays report-only.

## Hard rules

1. **Every finding cites its `scip-query` command** (or helper invocation).
2. **Verify before suggesting deletion** (`refs`/`affected`); flag framework entrypoints
   (Next.js `instrumentation.ts`/`proxy.ts`, route files, barrels) as false positives.
3. **Token estimates are bytes/4** — a relative ranking signal, not an exact count. Say so.
4. **Don't chase numbers.** A split/merge is worth it only if it preserves behavior and the new
   boundary is a real domain seam.
5. **Report-only.** Apply changes only on explicit request, then run `scip-verify`.
6. Extensible: add a new lens by appending another `sections[]` entry — the renderer and schema
   need no changes ("e por aí vai").
