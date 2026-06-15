# Output targets — rendering the refined demand

The refined demand is one thing; where it lives is another. Produce the content
once (per `output-template.md`), then render it to the chosen target. Detect the
target from context (a repo → Markdown/GitHub; an Atlassian workspace or a PROJ-123
key → Jira) or ask. When a connector for the tracker is available, offer to create
the item directly; otherwise hand over a clean, ready-to-paste document.

## Markdown file (repos, wikis, docs)

The default and most portable. Emit the template verbatim as a `.md` file.
- Mermaid fenced blocks render in GitHub/GitLab and many viewers; PlantUML usually
  needs a plugin, so for plain Markdown prefer Mermaid or also attach an image.
- Good when the demand should live next to the code (e.g. `docs/demands/<slug>.md`).

## GitHub issue

GitHub-flavored Markdown, with issue idioms:
- **Title** = the demand title. **Body** = the template sections.
- Render acceptance criteria and open questions as **task lists** so they're
  checkable: `- [ ] [BLOCKING] …`.
- ` ```mermaid ` blocks **render natively** in issue bodies — embed diagrams inline.
- Map metadata to **labels** (e.g. `needs-refinement` when NOT READY) and
  **milestones**; put sliced-out stories in **separate linked issues** and
  reference them (`- [ ] #123`).
- If a GitHub connector/tool is available, offer to open the issue(s); otherwise
  output the title + body block for pasting.

## Jira issue

Jira does not use GitHub Markdown. Render via the Atlassian tooling when connected
(the `Atlassian:createJiraIssue` / `editJiraIssue` tools accept a `contentFormat`
of `markdown` or `adf`); otherwise produce a paste-ready block and tell the user
which field each part goes in.
- **Summary** = demand title. **Description** = Summary/Goal/Scope/Assumptions.
- **Issue type**: Story for a feature, Bug for a defect; an over-sized demand
  (gate verdict TOO BIG) becomes an **Epic** with the slices as child Stories.
- Put the EARS rules and Given-When-Then scenarios in the **Acceptance Criteria**
  field (or a description section if there's no such field); keep Gherkin inside a
  `{code}` / code block so it's monospaced.
- Open questions → a checklist in the description, or **sub-tasks** for blocking
  ones so they're tracked to closure.
- Diagrams: Jira Cloud renders Mermaid/PlantUML only with a marketplace app, so
  include the source in a code block **and** export an image to attach when an app
  isn't present.
- Map the gate verdict to a label/status (e.g. `not-ready`) and never silently mark
  a NOT-READY demand as ready.

## Generic / other trackers (Linear, ClickUp, Azure DevOps, …)

Fall back to clean Markdown and state the field mapping explicitly: title →
title/summary; sections → description; rules + scenarios → acceptance criteria;
open questions → checklist or sub-items; verdict → a label or status. Use the
tracker's connector if one is available.

## Cross-target rules

- The **content is identical** across targets — only formatting and field mapping
  change. Never weaken the requirements to fit a target.
- Always carry the **readiness verdict** and the **open-questions list** into the
  target; they are the most valuable part of the hand-off.
- Diagrams travel as source first (portable, diffable); add a rendered image only
  where the target can't render the source.
