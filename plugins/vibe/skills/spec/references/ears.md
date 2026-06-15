# EARS — Easy Approach to Requirements Syntax

EARS (Mavin et al., Rolls-Royce, RE'09) constrains a requirement to a fixed clause
order so that the trigger, precondition/state, the system, and the response are all
explicit. Ambiguity has nowhere to hide. Use it to rewrite every business rule from
Phase 1.

## General structure and ruleset

```
WHILE <optional precondition(s)>, WHEN <optional trigger>, the <system name> SHALL <system response>
```

A valid EARS requirement has:
- zero or many preconditions
- zero or one trigger
- exactly one system name
- one or many responses

Clauses always appear in that order. Which keywords are present determines the
pattern.

## The five patterns (+ complex)

**Ubiquitous** — always active, no keyword. A fundamental property.
> The `<system>` shall `<response>`.
> *Example: The payment service shall record every transaction in the audit log.*

**Event-driven** — triggered when and only when an event occurs. Keyword **WHEN**.
> When `<trigger>`, the `<system>` shall `<response>`.
> *Example: When the customer confirms the order, the checkout shall send a confirmation e-mail within 30 seconds.*

**State-driven** — active while a state holds. Keyword **WHILE**.
> While `<state>`, the `<system>` shall `<response>`.
> *Example: While the account is suspended, the portal shall reject all login attempts.*

**Unwanted behavior** — required response to undesired situations (errors, invalid
input, failures). Keywords **IF / THEN**. Capturing these is how you write the
"what must NOT happen" rules that authors forget.
> If `<trigger>`, then the `<system>` shall `<response>`.
> *Example: If the uploaded file exceeds 10 MB, then the system shall reject it and display "file too large".*

**Optional feature** — applies only to variants that include a feature. Keyword
**WHERE**.
> Where `<feature is included>`, the `<system>` shall `<response>`.
> *Example: Where express delivery is enabled, the cart shall show an estimated arrival date.*

**Complex** — combine keywords for richer behavior.
> While `<state>`, when `<trigger>`, the `<system>` shall `<response>`.
> *Example: While the user is in guest mode, when they add a 4th item to the cart, the store shall prompt them to create an account.*

## Choosing a pattern

- Is it always true regardless of state or event? → **Ubiquitous**.
- Does an event/action kick it off? → **Event-driven (WHEN)**.
- Is it true for the whole duration of some state? → **State-driven (WHILE)**.
- Is it the response to something going wrong / invalid? → **Unwanted (IF/THEN)**.
- Only in some product variants/configs? → **Optional (WHERE)**.

A "ubiquitous-looking" requirement is often actually event-driven — push on it:
*what causes this to happen?* If there is a trigger, name it.

## Converting vague prose to EARS

**Example 1**
Vague: "The search should be fast and return good results."
Problems: "fast" and "good" are untestable.
EARS: "When the user submits a query of at least 3 characters, the search shall
return results within 1 second, sorted by relevance score."
(If "1 second" / "relevance score" can't be confirmed → raise a BLOCKING question.)

**Example 2**
Vague: "Users can't do stuff after their trial ends."
EARS (unwanted/state): "While the trial period has expired and no plan is active,
the app shall disable document editing and display the upgrade prompt."

**Example 3**
Vague: "Handle bad logins."
EARS (unwanted): "If the password is entered incorrectly 5 times within 15 minutes,
then the system shall lock the account for 30 minutes and notify the account owner
by e-mail."
(The numbers 5 / 15 / 30 are themselves candidate BLOCKING questions if not given.)

Note: keep the EARS clause order even when writing in another language. In
Portuguese, the keyword mapping is roughly WHEN→Quando, WHILE→Enquanto, IF/THEN→Se/
então, WHERE→Onde/Caso, SHALL→deve.
