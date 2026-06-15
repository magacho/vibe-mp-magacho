# Scenarios — Given / When / Then

Each example from Phase 1 (and each edge case from Phase 3) becomes a scenario. A
scenario is simultaneously an acceptance criterion (it states agreed behavior) and
the definition of an acceptance test (it states how to verify it). Good scenarios
are precise: one context, one action, one expected outcome.

## Structure

```
Scenario: <short, descriptive name>
  Given <the starting context / preconditions>
  When  <the single action / event>
  Then  <the expected, observable outcome>
```

- **Given** sets state — what is true before. Multiple Givens joined with **And**.
- **When** is the single trigger. Keep it to one action; two Whens usually means
  two scenarios.
- **Then** is an observable result, not an internal step. If you can't observe it,
  it isn't testable — and an untestable criterion fails the readiness gate.

## Worked example

```
Scenario: Reject oversized upload
  Given the user is on the document upload screen
  And the maximum upload size is 10 MB
  When the user selects a file of 12 MB
  Then the system rejects the file
  And displays the message "file too large (max 10 MB)"
  And no document is created
```

Note the negative assertion ("no document is created") — pair positive outcomes
with what must NOT happen.

## Cover the three kinds

For each rule, make sure you have scenarios for:
- **Happy path** — the intended successful flow.
- **Edge** — boundaries and unusual-but-valid cases (from the edge checklist).
- **Error** — invalid input and failure handling (the IF/THEN / unwanted rules).

## Multiple data points: Scenario Outline

When the same behavior should be checked across several values, use an outline with
an examples table instead of copy-pasting scenarios:

```
Scenario Outline: Password length validation
  Given the user is creating a password
  When they submit a password of length <length>
  Then the system shall <result>

  Examples:
    | length | result                          |
    | 7      | reject with "too short"         |
    | 8      | accept                          |
    | 64     | accept                          |
    | 65     | reject with "too long"          |
```

This is also a fast way to make boundary coverage visible (7/8 and 64/65 are the
edges that matter).

## Tips

- Name scenarios so a reader scanning the list understands coverage at a glance.
- Use concrete values, not "valid data" / "some amount".
- One scenario should fail for exactly one reason. If a scenario tests two things,
  split it.
- Write scenarios in the demand's language; keep Given/When/Then (or
  Dado/Quando/Então in Portuguese) consistent throughout.
