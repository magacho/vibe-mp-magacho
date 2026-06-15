# vibe-mp-magacho

Marketplace de skills do toolset **vibe** — para Claude Code, Cowork e Claude Desktop / claude.ai, e portável pra outras ferramentas que leem `SKILL.md` (ex.: OpenClaw).

Plugin `vibe`, com duas skills:
- **`spec`** — refina uma demanda em especificação pronta pra construir (Example Mapping, EARS, edge cases, Gherkin, portão de prontidão). Handle: `vibe:spec`.
- **`modular`** — projeta ou refatora código em módulos de baixo acoplamento (modo legado + modo projeto novo). Handle: `vibe:modular`.

## Estrutura

```
.claude-plugin/marketplace.json     # registry lido pelo Claude Code / Cowork
plugins/vibe/
  .claude-plugin/plugin.json        # versão = fonte da verdade
  skills/
    spec/SKILL.md                   # (placeholder — substituir)
    modular/SKILL.md                # (placeholder — substituir)
scripts/
  validate.sh                       # valida manifestos + frontmatter (usa python3)
  build-zips.sh                     # gera os .zip de release
.github/workflows/
  ci.yml                            # valida em todo PR / push na main
  release.yml                       # dispara ao criar tag vX.Y.Z
```

## Colocando os arquivos das skills

1. Substitua o conteúdo de `plugins/vibe/skills/spec/` pelos arquivos reais do `requirement-refiner`.
2. Substitua o conteúdo de `plugins/vibe/skills/modular/` pelos arquivos reais do `code-modularization`.
3. Em cada `SKILL.md`, ajuste o frontmatter `name:` para `spec` / `modular` (os arquivos vêm com os nomes longos).
4. Rode `bash scripts/validate.sh` localmente — tem que passar.

## Lançando uma release

```bash
# 1. bump da versão (fonte da verdade): edite "version" em
#    plugins/vibe/.claude-plugin/plugin.json   (ex.: 0.1.0 -> 0.2.0)
# 2. commit + tag IGUAL à versão
git commit -am "release: vibe 0.2.0"
git tag v0.2.0
git push origin main --tags
```

O workflow valida a estrutura, confere que a tag bate com o `plugin.json`, gera os zips e publica a Release com eles anexados.

Artefatos gerados por release:
- `spec-vX.Y.Z.zip`, `modular-vX.Y.Z.zip` → upload de **skill** em claude.ai / Claude Desktop (chat).
- `vibe-plugin-vX.Y.Z.zip` → upload de **plugin** no Cowork / Claude Desktop (Personal plugins).

## Instalando

**Claude Code / Cowork (via marketplace):**
```bash
claude plugin marketplace add https://github.com/magacho/vibe-mp-magacho
claude plugin install vibe@vibe-mp
```

**claude.ai / Claude Desktop (chat):** Customize → Skills → `+` → upload do `.zip` da skill (da Release).
No chat/web não há auto-update — re-suba o `.zip` pra atualizar.

## Usando em outras ferramentas (OpenClaw etc.)

As skills são `SKILL.md` autocontidos (frontmatter `name` + `description` + corpo markdown), então portam sem conversão pra qualquer agente que leia esse formato. No OpenClaw, por exemplo:
- aponte um skill root pro clone deste repo (a descoberta é recursiva e acha os `SKILL.md` em `plugins/vibe/skills/`), **ou**
- copie as pastas `spec/` e `modular/` (ou o conteúdo dos zips de skill) pra `~/.openclaw/workspace/skills/`.

O nome da skill vem do campo `name` do frontmatter, então o handle continua `spec` / `modular`. Só o invólucro do Claude (`.claude-plugin/`, `claude plugin install`) é que não se aplica fora do ecossistema Claude.
