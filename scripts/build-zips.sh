#!/usr/bin/env bash
# Builds release artifacts:
#   - per-skill zips  -> for claude.ai / Claude Desktop (chat) skill upload
#   - per-plugin zips -> for Cowork / Claude Desktop "Personal plugins" upload
# Each artifact also bundles the matching usage docs from docs/ when present:
#   - per-skill: docs/<skill>.md is copied in as <skill>/USAGE.md
#   - per-plugin: the whole docs/ folder rides along at the top level
# Usage: scripts/build-zips.sh <version>
set -euo pipefail
VERSION="${1:?usage: build-zips.sh <version>}"
ROOT="$(pwd)"; DIST="$ROOT/dist"; STAGE="$ROOT/.build-stage"
rm -rf "$DIST" "$STAGE" && mkdir -p "$DIST"
trap 'rm -rf "$STAGE"' EXIT
shopt -s nullglob

# per-skill zips: skill folder + its usage doc
for d in plugins/*/skills/*/; do
  name=$(basename "$d")
  rm -rf "$STAGE" && mkdir -p "$STAGE/$name"
  cp -R "$d." "$STAGE/$name/"
  [ -f "docs/${name}.md" ] && cp "docs/${name}.md" "$STAGE/$name/USAGE.md"
  ( cd "$STAGE" && zip -rq "$DIST/${name}-v${VERSION}.zip" "$name" )
  echo "built ${name}-v${VERSION}.zip"
done

# per-plugin zips: plugin folder + docs/ at the top level
for p in plugins/*/; do
  name=$(basename "$p")
  rm -rf "$STAGE" && mkdir -p "$STAGE"
  cp -R "$p" "$STAGE/$name"
  args=("$name")
  if [ -d docs ]; then cp -R docs "$STAGE/docs"; args+=(docs); fi
  ( cd "$STAGE" && zip -rq "$DIST/${name}-plugin-v${VERSION}.zip" "${args[@]}" )
  echo "built ${name}-plugin-v${VERSION}.zip"
done
