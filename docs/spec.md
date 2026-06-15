# Skill `spec` — Requirement Refiner

> Handle: `vibe:spec` · Foco: **requisitos**, não solução técnica nem estimativa.

Refina uma demanda (user story, pedido de feature ou requisito já formatado)
**antes** de qualquer quebra técnica, caçando áreas de sombra — o que o autor
assumiu, nunca pensou ou deixou vago — e decidindo se a demanda está **pronta
para construir**.

A ideia central: *refinar é caçar o que falta, não polir o que já está lá.* O
valor da skill está nas perguntas que ela levanta, e ela termina com um veredito
explícito de prontidão (Definition of Ready) em vez de fingir que está tudo
resolvido.

## Quando usar

- Você recebeu uma demanda e quer saber **o que está faltando** antes de começar.
- Precisa de **critérios de aceitação** testáveis, não de um parágrafo vago.
- Quer **edge cases** e comportamentos indesejados que ninguém mapeou ainda.
- Quer transformar exemplos em **cenários Given-When-Then** que servem como
  critério de aceitação e teste ao mesmo tempo.
- Precisa decidir, com critério objetivo, se a demanda **está pronta** ou precisa
  de mais refinamento — ou se é grande demais e deve ser **quebrada**.

Gatilhos típicos: *detalhamento de demanda, refinamento de requisitos, critérios
de aceitação, cenários, casos de teste, áreas de sombra, Example Mapping,
Definition of Ready, EARS, INVEST, Gherkin.*

## Quando NÃO usar

- Você quer **design de arquitetura, quebra em tarefas ou estimativa** — a skill
  para no requisito de propósito. Para arquitetura/modularização, use
  [`modular`](./modular.md).
- A demanda já está madura e testável, sem perguntas bloqueantes — não há sombra
  para caçar.

## Como invocar

- **Claude Code / Cowork:** referencie o handle `vibe:spec`, ou simplesmente
  descreva a tarefa ("refina essa demanda", "quais os edge cases disso?", "isso
  está pronto pra dev?") — a skill é disparada pela descrição.
- **claude.ai / Desktop (chat):** com a skill `spec` instalada, cole a demanda e
  peça o refinamento.

## O que ela faz (o loop de refinamento)

| Fase | O que acontece |
|------|----------------|
| 0 — Intake | Reformula o núcleo em uma frase (quem / o quê / por quê), separa o que é dado do que é suposição. |
| 1 — Map | Example Mapping: regras, exemplos concretos, perguntas (marcadas BLOCKING/DEFERRABLE) e novas histórias. |
| 2 — Sharpen | Reescreve regras em sintaxe **EARS** e caça termos vagos (*rápido, simples, vários…*), quantificando ou virando pergunta bloqueante. Adiciona requisitos negativos. |
| 3 — Edge sweep | Varredura sistemática de edge cases (entrada vazia/inválida, limites, concorrência, permissões, estado, falhas, escala). |
| 4 — Scenarios | Converte exemplos em cenários Given-When-Then (Gherkin) — critério de aceitação + teste. |
| 5 — Visualize | Gera diagramas (use-case, sequência, atividade, estado) como diagram-as-code (Mermaid/PlantUML) quando esclarecem. |
| 6 — Readiness gate | Veredito único: **NOT READY**, **TOO BIG / SPLIT** ou **READY**. |
| 7 — Render | Renderiza para o destino: arquivo Markdown, issue do Jira, issue do GitHub ou outro tracker. |

O veredito é o coração da skill — a distinção **BLOCKING** (responder errado causa
retrabalho/constrói a coisa errada) vs **DEFERRABLE** (qualquer escolha razoável
serve, barato mudar depois) decide se para ou continua.

---

## Exemplo de uso

**Entrada (demanda crua):**

> "Como usuário, quero poder exportar meu relatório para que eu possa
> compartilhá-lo."

**O que a skill produz (resumido):**

**Fase 0 — Restate:** *Como usuário autenticado, quero exportar um relatório em
arquivo para compartilhá-lo fora do sistema.* (Suposição: "exportar" = gerar
arquivo, não enviar por e-mail.)

**Fase 1 — Map (trecho):**
- Regra: o usuário pode exportar um relatório que ele tem permissão de ver.
  - Exemplo: relatório de 1.000 linhas → arquivo baixado.
- Pergunta **BLOCKING**: quais formatos? (CSV, PDF, XLSX mudam tudo.)
- Pergunta **BLOCKING**: relatório vazio (0 linhas) — exporta arquivo vazio ou erro?
- Pergunta **DEFERRABLE**: nome default do arquivo.
- Nova história: *enviar relatório por e-mail* (incremento separado — fatiar).

**Fase 2 — EARS (depois de "formato = CSV e PDF" respondido):**
- `WHEN o usuário solicita exportar um relatório que pode visualizar, the system SHALL gerar o arquivo no formato escolhido (CSV ou PDF) em até 5 segundos para relatórios de até 10.000 linhas.`
- Negativo: `the system SHALL NOT incluir colunas que o usuário não tem permissão de ver.`

**Fase 4 — Cenário:**
```gherkin
Cenário: exportar relatório vazio
  Dado um relatório ao qual o usuário tem acesso e que não contém linhas
  Quando ele solicita a exportação em CSV
  Então o sistema gera um arquivo CSV apenas com o cabeçalho
  E exibe o aviso "Relatório sem dados no período".
```

**Fase 6 — Veredito:** `NOT READY` enquanto os formatos não forem definidos →
devolve a lista numerada de perguntas bloqueantes. Respondidas, re-entra no loop
e fecha em `READY`, listando suposições registradas e perguntas adiáveis.

---

## Cenários onde a skill faz sentido

1. **Grooming / refinamento de backlog.** Um PO traz uma história vaga; a skill
   devolve regras em EARS, cenários e a lista exata de perguntas bloqueantes para
   levar à conversa com o time — em vez de chutar e registrar cinco suposições
   frágeis.

2. **"Está pronto para a sprint?"** Antes de puxar um card para a sprint, rodar a
   skill aplica um Definition of Ready objetivo: ou passa no gate, ou diz
   exatamente o que falta.

3. **Epic disfarçado de história.** A demanda mistura várias capacidades
   independentes. A skill detecta o tamanho (veredito `TOO BIG / SPLIT`) e propõe
   o fatiamento em incrementos INVEST antes de tentar refinar o todo.

4. **Caça a edge cases em feature crítica.** Pagamento, autenticação, limites de
   quota — onde o custo de esquecer um caso é alto. A varredura sistemática da
   Fase 3 traz à tona os comportamentos indesejados e os caminhos de erro.

5. **Geração de critérios de aceitação testáveis.** O time quer cenários
   Given-When-Then que sirvam direto como base de testes de aceitação, já ligados
   às regras.

6. **Documentar a demanda no tracker certo.** Ao final, renderiza para issue do
   Jira/GitHub ou arquivo Markdown, com diagramas embutidos — pronto para colar
   ou criar via conector.

## Dica

O caminho mais rápido até `READY` costuma ser **responder as 2–5 perguntas
bloqueantes** que a skill levanta, em vez de deixá-la supor. Trate-a como uma
conversa, não como um gerador de documento de uma tacada.
