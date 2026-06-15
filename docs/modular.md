# Skill `modular` — Code Modularization

> Handle: `vibe:modular` · Norte: **cada mudança toca um módulo, então cada
> mudança só precisa daquele módulo carregado no contexto.**

Projeta ou refatora um código em módulos de baixo acoplamento, com fronteiras
claras e dependências fluindo em uma direção só. O objetivo é que corrigir um bug
ou adicionar uma feature signifique abrir **uma caixa bem definida** em vez do
sistema inteiro — tanto para humanos navegando o código quanto para uma IA
trabalhando dentro de uma janela de contexto limitada.

## Os dois modos

Identifique o modo **antes de qualquer coisa** — o risco dominante é oposto em
cada um:

- **Modo A — Refatorar projeto existente.** Já há código funcionando (muitas
  vezes legado, pouco testado). Diretiva principal: **preservar comportamento** —
  mover código, não reescrever. O perigo é a **regressão silenciosa**.
- **Modo B — Arquitetar projeto novo.** Pouco ou nenhum código ainda; você atua
  como arquiteto, desenhando fronteiras e contratos. O perigo é o oposto:
  **over-engineering** e abstração prematura.

Se for ambíguo (ex.: "protótipo pequeno que queremos crescer"), a skill pergunta
qual encaixa, ou trata como um Modo A pequeno seguido de planejamento Modo B.

## O que faz um bom módulo

- **Responsabilidade única e nomeável** — se você não descreve em uma frase sem
  "e", provavelmente são dois módulos.
- **Superfície pública pequena** — expõe só o necessário; o resto fica privado.
- **Dependência em uma direção** — módulos de baixo nível (utils, tipos, domínio)
  não importam os de alto nível (features, páginas, entrypoints).
- **Agrupa o que muda junto** (alta coesão); separa o que muda por razões
  diferentes.
- **Nunca forma ciclo** — A importa B e B importa A (direto ou via cadeia) é a
  maior causa de um código parecer "emaranhado". Ciclos são o que caçar no Modo A
  e tornar estruturalmente impossível no Modo B.

## Quando usar

- "Esse arquivo está grande demais" / "quero quebrar esse arquivo".
- "Tem dependência demais entre essas partes" / "esse código está emaranhado".
- "Me ajuda a organizar esse código" / "revisa as fronteiras dos módulos".
- "Desenha a arquitetura de um projeto novo com modularidade em mente".
- "Ensina o Claude a trabalhar em módulos aqui."

> Os gatilhos valem **mesmo sem a palavra "modularizar"**.

## Quando NÃO usar

- Você quer refinar **o que** construir (requisitos/critérios) — isso é a skill
  [`spec`](./spec.md). `modular` cuida do **como** estruturar o código.
- Uma mudança trivial e localizada que não tem nada a ver com fronteiras de
  módulo.

## Como invocar

- **Claude Code / Cowork:** referencie `vibe:modular` ou descreva o problema de
  estrutura — a skill é disparada pela descrição.
- **claude.ai / Desktop (chat):** com a skill `modular` instalada, aponte o
  arquivo/projeto e descreva o objetivo (untangle vs. arquitetar do zero).

## O checkpoint obrigatório: apresentar antes de agir

Em **ambos os modos** vale uma regra dura: **apresentar o plano — estrutura,
impactos e riscos — e ter uma conversa real com o usuário antes de mudar
qualquer coisa.** Não é um diálogo de confirmação; é uma conversa. O usuário sabe
coisas que o código não mostra (por que um arquivo "bagunçado" é assim, o que é
frágil, o que vai ser jogado fora mesmo). Para planos grandes, combina-se um
**piloto** — um módulo —, valida-se junto e só então segue.

## Verificação mecânica de fronteiras

"Acho que as dependências estão ok" é exatamente o julgamento que perde um ciclo
de três saltos. Quando a linguagem é conhecida, a skill usa ferramentas concretas
(`references/dependency-tools.md`) para detectar acoplamento e ciclos
automaticamente — no Modo A para achar ciclos, no Modo B para confirmar que a nova
estrutura não tem nenhum.

## O payoff persistente

Uma limpeza única decai se o trabalho futuro não respeitar as fronteiras. Ao
final, a skill captura as regras do projeto para que persistam: lista de módulos e
a responsabilidade de cada um, direções de import permitidas e a superfície
pública de cada módulo (ver `references/environment-setup.md`, que cobre Claude
Code e Claude.ai).

---

## Exemplos de uso

### Modo A — untangle de um arquivo legado

**Entrada:** "Esse `app.py` tem 2.000 linhas e mexer em qualquer coisa quebra
outra. Ajuda a organizar."

**O que a skill faz:**
1. Identifica Modo A → diretiva: **preservar comportamento**.
2. Mapeia responsabilidades misturadas no arquivo (rotas HTTP, regras de negócio,
   acesso a banco, helpers de formatação) e roda detecção de ciclos.
3. **Apresenta o plano antes de tocar no código:** propõe extrair `db/`,
   `domain/`, `routes/`, `utils/`; mostra o blast radius e o risco de regressão;
   sugere um **piloto** (extrair só `utils/` primeiro) para validar.
4. Move o código (não reescreve), mantendo a fachada pública.
5. Confirma com ferramenta que não sobraram ciclos e registra as regras de import.

### Modo B — arquitetura de projeto novo

**Entrada:** "Vou começar uma API de cobrança do zero, quero que já nasça
modular."

**O que a skill faz:**
1. Identifica Modo B → risco: **over-engineering**.
2. Desenha fronteiras por responsabilidade (`billing`, `payments`, `notifications`,
   `shared/types`) e contratos entre elas, com dependências apontando só para
   baixo.
3. **Apresenta tradeoffs e reversibilidade** antes de gerar estrutura — evita
   abstração prematura, prefere o mínimo que mantém ciclos impossíveis.
4. Gera o esqueleto e configura a verificação mecânica de fronteiras desde o
   início.
5. Persiste as regras de módulo para o trabalho futuro respeitar.

---

## Cenários onde a skill faz sentido

1. **Arquivo-monstro.** Um único arquivo concentra responsabilidades demais e
   virou gargalo — toda mudança exige carregar tudo no contexto. (Modo A)

2. **Código emaranhado / acoplamento alto.** Mudar A quebra B e C sem relação
   óbvia; há suspeita de ciclos de import. A skill detecta os ciclos
   mecanicamente e propõe o módulo compartilhado que falta. (Modo A)

3. **Reduzir contexto para IA.** O objetivo explícito é que o Claude (ou qualquer
   agente) consiga trabalhar abrindo poucos arquivos — fronteiras pequenas e
   one-way reduzem o que precisa entrar na janela de contexto. (A ou B)

4. **Projeto novo nascendo certo.** Antes de escrever a primeira feature, desenhar
   módulos e contratos para o projeto começar modular — sem cair no
   over-engineering. (Modo B)

5. **Revisão de fronteiras.** O time quer auditar se os limites de módulo atuais
   fazem sentido, onde está o acoplamento indevido e quais imports violam a
   direção permitida. (A)

6. **"Ensinar o Claude a trabalhar em módulos aqui."** Capturar as regras do
   projeto (módulos, direções de import, superfícies públicas) para que sessões
   futuras e o trabalho do time respeitem as fronteiras. (A ou B)

## Dica

Não confie no olho para dependências — peça a verificação mecânica de ciclos. E
não pule o checkpoint: o plano apresentado antes de mexer é onde o conhecimento
que só o usuário tem corrige o desenho **antes** de causar dano, não depois.
