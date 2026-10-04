# ADR-0001: Status fields use enums

**Status:** Accepted
**Date:** 2026-08-10
**Note:** This entry was drafted with AI assistance (Claude), then reviewed
and approved by Chloe Walker, consistent with the AI Assistance policy in
docs/PROJECT_CONTEXT.md.

## Context

Three fields track "what state something is in": `Quest.status`,
`Monster.threat_level`, and `Character.status`. Each handled validation
differently:

- `Quest.status` and `Monster.threat_level` used a plain text column plus a
  `CheckConstraint` that listed the allowed values as a raw SQL string.
- Two Python enum classes (`QuestStatus`, `MonsterThreatLevel`) already
  existed in the code, listing those same allowed values -- but were never
  actually connected to a column. They did nothing.
- `Character.status` had no validation at all. Any text was accepted.

So the same idea ("these are the only valid values") was defined in two
different places for two of the fields, and not defined at all for the
third.

## Decision

Use SQLAlchemy's `Enum` column type everywhere a field represents a fixed
set of states. This connects a Python enum class directly to the database
column, so there's only one place the valid values are ever listed. A new
`CharacterStatus` enum was added (`alive`, `deceased`, `missing`) to fix
the gap on `Character.status`. The old `CheckConstraint`s were removed,
since the enum now provides the same protection.

## Consequences

- Added: a `CharacterStatus` enum.
- Removed: the two `CheckConstraint`s for quest status and monster threat
  level.
- A surprise along the way: SQLAlchemy's `Enum` type checks values against
  an enum member's *name* by default (e.g. `ALIVE`), not its *value* (e.g.
  `"alive"`). Since the rest of the app already used lowercase strings like
  `"alive"`, every enum column needed one extra setting
  (`values_callable=lambda x: [e.value for e in x]`) to match against the
  lowercase values instead. This was found by an actual test failure, not
  planned for ahead of time.
- Not done: updating the API layer to use real `CharacterStatus` values
  instead of plain strings. That's a bigger change, left for later.
- Option considered and rejected: keep the `CheckConstraint`s and just
  delete the unused enum classes. Rejected because it does not fix the
  real problem -- adding a new valid value would still mean hand-editing a
  raw SQL string.