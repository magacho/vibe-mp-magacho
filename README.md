# vibe-mp-magacho

Marketplace de skills do toolset **vibe** — para Claude Code, Cowork e Claude Desktop / claude.ai, e portável pra outras ferramentas que leem `SKILL.md` (ex.: OpenClaw).

Plugin `vibe`, com duas skills:
- **`spec`** — refina uma demanda em especificação pronta pra construir (Example Mapping, EARS, edge cases, Gherkin, portão de prontidão). Handle: `vibe:spec`. → [documentação](docs/spec.md)
- **`modular`** — projeta ou refatora código em módulos de baixo acoplamento (modo legado + modo projeto novo). Handle: `vibe:modular`. → [documentação](docs/modular.md)

Cada doc traz quando usar (e quando não), como invocar, exemplos de uso e cenários onde a skill faz sentido.

## Estrutura

```
.claude-plugin/marketplace.json     # registry lido pelo Claude Code / Cowork
plugins/vibe/
  .claude-plugin/plugin.json        # versão = fonte da verdade
  skills/
    spec/SKILL.md                   # skill spec + references/
    modular/SKILL.md                # skill modular + references/
scripts/
  validate.sh                       # valida manifestos + frontmatter (usa python3)
  build-zips.sh                     # gera os .zip de release
.github/workflows/
  ci.yml                            # valida em todo PR / push na main
  release.yml                       # dispara ao criar tag vX.Y.Z
docs/
  spec.md                           # doc da skill spec (uso + cenários)
  modular.md                        # doc da skill modular (uso + cenários)
```

## Instalando

### Claude Code / Cowork (via marketplace)

A forma recomendada — instala o plugin completo e recebe updates ao re-rodar `install`:

```bash
claude plugin marketplace add https://github.com/magacho/vibe-mp-magacho
claude plugin install vibe@vibe-mp
```

Depois, as skills ficam disponíveis pelos handles `vibe:spec` e `vibe:modular`.

### claude.ai / Claude Desktop (chat)

Baixe os `.zip` de skill da [última Release](https://github.com/magacho/vibe-mp-magacho/releases/latest) e suba em **Customize → Skills → `+`**:

- `spec-vX.Y.Z.zip` — skill `spec`
- `modular-vX.Y.Z.zip` — skill `modular`

No chat/web não há auto-update — re-suba o `.zip` da nova versão para atualizar.

### Plugin pessoal (Cowork / Desktop)

Use o `vibe-plugin-vX.Y.Z.zip` da Release em **Personal plugins**, que traz as duas skills de uma vez.

### Outras ferramentas (OpenClaw etc.)

As skills são `SKILL.md` autocontidos — veja [Usando em outras ferramentas](#usando-em-outras-ferramentas-openclaw-etc) abaixo.

## Lançando uma release

```bash
# 1. bump da versão (fonte da verdade): edite "version" em
#    plugins/vibe/.claude-plugin/plugin.json   (ex.: 0.2.0 -> 0.3.0)
#    e mantenha marketplace.json em sincronia
# 2. commit + tag IGUAL à versão
git commit -am "release: vibe 0.3.0"
git tag v0.3.0
git push origin main --tags
```

O workflow valida a estrutura, confere que a tag bate com o `plugin.json`, gera os zips e publica a Release com eles anexados.

Artefatos gerados por release:
- `spec-vX.Y.Z.zip`, `modular-vX.Y.Z.zip` → upload de **skill** em claude.ai / Claude Desktop (chat).
- `vibe-plugin-vX.Y.Z.zip` → upload de **plugin** no Cowork / Claude Desktop (Personal plugins).

## Usando em outras ferramentas (OpenClaw etc.)

As skills são `SKILL.md` autocontidos (frontmatter `name` + `description` + corpo markdown), então portam sem conversão pra qualquer agente que leia esse formato. No OpenClaw, por exemplo:
- aponte um skill root pro clone deste repo (a descoberta é recursiva e acha os `SKILL.md` em `plugins/vibe/skills/`), **ou**
- copie as pastas `spec/` e `modular/` (ou o conteúdo dos zips de skill) pra `~/.openclaw/workspace/skills/`.

O nome da skill vem do campo `name` do frontmatter, então o handle continua `spec` / `modular`. Só o invólucro do Claude (`.claude-plugin/`, `claude plugin install`) é que não se aplica fora do ecossistema Claude.
