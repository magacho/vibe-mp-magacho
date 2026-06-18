#!/usr/bin/env bash
# Preflight for codebase-360: detect required/optional tooling and print install guidance.
# Exit 0 = ready to run. Exit 1 = a REQUIRED tool is missing (see hints above).
export PATH="$HOME/.local/bin:$PATH"

miss_required=0
say() { printf '%s\n' "$1"; }

say "== Codebase 360 preflight =="

# --- REQUIRED: scip-query CLI ---
if command -v scip-query >/dev/null 2>&1; then
  say "OK   scip-query ($(scip-query --version 2>/dev/null | head -1))"
else
  miss_required=1
  say "MISS scip-query  → install:  npm install -g scip-query"
  say "                  (or run the scip-polyglot-setup skill, which installs it for you)"
fi

# --- REQUIRED: python3 (renders the deck) ---
if command -v python3 >/dev/null 2>&1; then
  say "OK   python3 ($(python3 --version 2>&1))"
else
  miss_required=1
  say "MISS python3  → install python3 (apt-get install -y python3 / brew install python3)"
fi

# --- REQUIRED for reindex: scip CLI + language indexers ---
if command -v scip-query >/dev/null 2>&1; then
  if scip-query check-deps >/tmp/c360-deps.txt 2>&1; then
    say "OK   scip indexers (scip-query check-deps passed)"
  else
    miss_required=1
    say "MISS scip CLI or a language indexer (scip-query check-deps failed):"
    sed 's/^/       /' /tmp/c360-deps.txt | head -20
    say "       → run the scip-polyglot-setup skill to install the scip CLI + indexers"
  fi
fi

# --- OPTIONAL: headless browser for screenshots (deck still renders without it) ---
if command -v google-chrome >/dev/null 2>&1 || command -v chromium >/dev/null 2>&1 \
   || command -v chromium-browser >/dev/null 2>&1; then
  say "OK   headless browser (visual verification available)"
else
  say "WARN no chrome/chromium → step 5 screenshot skipped; HTML still opens in any browser"
fi

# --- OPTIONAL: bemobi-brand skill for the logo (text fallback otherwise) ---
brand=$(ls "$HOME"/.claude/plugins/cache/bemobi-marketplace/bemobi-skills/*/skills/bemobi-brand/assets/logos/logo-horizontal-black.svg 2>/dev/null | head -1)
if [ -n "$brand" ]; then
  say "OK   bemobi-brand logo found"
else
  say "WARN bemobi-brand logo not found → deck uses a text 'bemobi' fallback"
fi

echo
if [ "$miss_required" -eq 1 ]; then
  say "RESULT: missing REQUIRED tooling — install the MISS items above before running."
  exit 1
fi
say "RESULT: ready to run codebase-360."
