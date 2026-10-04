# Architecture Decision Records

This folder contains Architecture Decision Records (ADRs) for MythosAI — one
file per significant, deliberate technical decision.

## Why these exist

`ENGINEERING_LOG.md` is chronological: it answers "what happened, and when."
ADRs are decision-indexed: they answer "why do we do X this way." Six months
from now, if you're wondering why a particular technology or pattern was
chosen, you shouldn't have to dig through a dated log to find out — you
should be able to look it up by topic.

## When to write one

Write an ADR when a decision is:
- **Significant** — it affects the architecture, not just a one-line fix
- **Deliberate** — real alternatives were considered, not just "the only option"
- **Likely to be questioned later** — someone (including future you) might
  reasonably ask "why did we do it this way?"

Not every commit needs one. A typo fix doesn't. Choosing `pydantic-settings`
over hand-written validation did.

## Numbering convention

Files are named `NNNN-short-title.md`, using a zero-padded, sequential
number (`0001`, `0002`, ...). Numbers are never reused, even if a decision
is later superseded — a superseded ADR stays in place with its status
updated to `Superseded by ADR-NNNN`, rather than being deleted.

`0000-template.md` is the template every new ADR should be copied from.

## Status values

- **Proposed** — under consideration, not yet acted on
- **Accepted** — the decision is in effect
- **Superseded by ADR-NNNN** — replaced by a later decision; kept for history