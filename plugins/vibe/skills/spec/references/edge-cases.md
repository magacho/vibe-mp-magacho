# Edge-case & unwanted-behavior checklist

Walk the demand through every category. The goal is not to invent improbable
science fiction — it is to ask, for each category, "has the demand said what
happens here?" If not, that is a shadow area: turn it into an example, a rule, or
a question. Skip a category only when you can articulate *why* it cannot apply.

## Input
- Empty input / nothing entered / no selection.
- Invalid format, wrong type, malformed data.
- Too long / too short; leading/trailing whitespace; special characters, emoji,
  other scripts/locales.
- Injection-shaped input (does the demand assume it's sanitized?).
- Duplicate submission / double-click / resubmit.

## Boundaries (test the edges, not the middle)
- Zero, one, the maximum, maximum+1, negative.
- Exactly at a threshold vs just over/under it.
- First item / last item / only item / none.
- Date boundaries: midnight, month/year rollover, timezones, DST, leap years.
- Money: 0,00, rounding, currency, very large amounts.

## State & lifecycle
- The "first run" / empty state (no data yet).
- Already-done / repeated action (idempotency).
- Out-of-order actions (doing step 3 before step 1).
- Stale state: the thing changed/was deleted since the screen loaded.
- Expired sessions, tokens, trials, subscriptions.

## Identity, permissions, multi-actor
- Not logged in / logged in / wrong role / insufficient permission.
- The actor acting on someone else's resource.
- Two users acting on the same resource at once (concurrency / race / conflict).
- Account states: new, suspended, deleted, guest vs registered.

## Errors & failures (the "what must NOT happen" rules)
- A dependency (API, DB, payment, third party) is slow, down, or returns an error.
- Partial success: step 1 succeeds, step 2 fails — what is the recovery / rollback?
- Timeout, retry, double-charge prevention.
- What does the *user* see and what is *logged* when it fails?

## Scale & performance
- Many items (long lists → pagination?), large files, high request volume.
- Slow network / offline / connection drops mid-action.

## Data & integrity
- Required vs optional fields; defaults; what is persisted vs derived.
- What happens to related/historical data when something is edited or deleted?
- Auditing: does this need to be traceable?

## Cross-cutting / non-functional (raise as rules or questions)
- Accessibility, localization/i18n, responsive/mobile.
- Privacy/PII, consent, regulatory constraints.
- Notifications: who is told, through which channel, when?
- Observability: what should be measurable/logged to know it works?

## Negative space
Ask directly: **what should this feature explicitly NOT do?** Out-of-scope items
belong in the doc as stated non-goals so they aren't silently built or assumed.
