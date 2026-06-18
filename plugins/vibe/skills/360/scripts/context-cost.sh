#!/usr/bin/env bash
# context-cost.sh — deterministic token/context-cost math for the scip-context-budget skill.
#
# Token estimate uses the bytes/4 heuristic (relative ranking signal, not exact).
#
# Subcommands:
#   tokens [path ...]        List source files with estimated tokens, largest first.
#                            No args -> scans ./src for ts/tsx/js/jsx/mts.
#   edit-cost <file>         Transitive internal-dependency closure of <file> via
#                            `scip-query deps`, with the total tokens the AI must load
#                            to safely edit it (file + closure). The headline metric.
#   closure <file>           Just the list of files in the edit closure (one per line).
#
# Requires `scip-query` on PATH for edit-cost/closure. `tokens` is pure filesystem.

set -uo pipefail
CMD="${1:-}"; shift || true
BYTES_PER_TOKEN=4

est_tokens() { # <file> -> echo token estimate
  local b; b=$(wc -c <"$1" 2>/dev/null || echo 0)
  echo $(( b / BYTES_PER_TOKEN ))
}

cmd_tokens() {
  local files=("$@")
  if [ ${#files[@]} -eq 0 ]; then
    mapfile -t files < <(find src -type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' -o -name '*.mts' \) 2>/dev/null)
  fi
  printf '%8s  %5s  %s\n' "TOKENS" "LOC" "FILE"
  for f in "${files[@]}"; do
    [ -f "$f" ] || continue
    printf '%8s  %5s  %s\n' "$(est_tokens "$f")" "$(wc -l <"$f")" "$f"
  done | sort -rn
}

# BFS transitive closure of internal deps
compute_closure() { # <file> -> prints closure files (incl. self) one per line
  local start="$1"
  declare -A seen
  local queue=("$start") f d
  while [ ${#queue[@]} -gt 0 ]; do
    f="${queue[0]}"; queue=("${queue[@]:1}")
    [ -n "${seen[$f]:-}" ] && continue
    seen[$f]=1
    while IFS= read -r d; do
      [ -z "$d" ] && continue
      [ -n "${seen[$d]:-}" ] || queue+=("$d")
    done < <(scip-query deps "$f" 2>/dev/null)
  done
  printf '%s\n' "${!seen[@]}"
}

cmd_closure() {
  [ -n "${1:-}" ] || { echo "usage: context-cost.sh closure <file>" >&2; exit 2; }
  compute_closure "$1" | sort
}

cmd_edit_cost() {
  [ -n "${1:-}" ] || { echo "usage: context-cost.sh edit-cost <file>" >&2; exit 2; }
  local target="$1" total=0 n=0 self
  self=$(est_tokens "$target")
  echo "Target: $target"
  echo "  self: ${self} tokens, $(wc -l <"$target" 2>/dev/null || echo 0) LOC"
  echo "  ── edit closure (file + transitive internal deps) ──"
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    local t; t=$(est_tokens "$f")
    total=$(( total + t )); n=$(( n + 1 ))
    printf '    %8s tok  %s\n' "$t" "$f"
  done < <(compute_closure "$target" | sort)
  echo "  ──────────────────────────────────────────────────"
  echo "  EDIT-CONTEXT COST: ${total} tokens across ${n} files"
  echo "  (this is what an AI must load to change ${target} safely)"
}

case "$CMD" in
  tokens)    cmd_tokens "$@" ;;
  edit-cost) cmd_edit_cost "$@" ;;
  closure)   cmd_closure "$@" ;;
  *) echo "usage: context-cost.sh {tokens|edit-cost <file>|closure <file>}" >&2; exit 2 ;;
esac
