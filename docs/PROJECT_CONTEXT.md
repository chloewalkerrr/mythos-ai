# MythosAI — Project Context

**Last updated:** 2026-08-08
**Status:** Living document — update when motivation, goals, or principles genuinely change, not on every code change.

---

## Purpose of this document

This document exists to answer one question for any reader (including future me): **why does this project exist, and what is it trying to prove?**

It intentionally does not describe how the system works today (`ARCHITECTURE.md`) or what's planned next (`ROADMAP.md` / `DEVELOPMENT_ROADMAP.md`). It describes intent, principles, and constraints that should stay stable even as the code changes significantly.

---

## Author

Chloe Walker

[TODO: add GitHub profile / LinkedIn / contact email here if you want this document to reference them directly.]

---

## What MythosAI is

MythosAI is an AI-powered knowledge and reasoning platform built on a structured model of the Percy Jackson universe. It began as a university Database Systems project (CMSC 4323) focused on relational database design, and is now being independently extended into a long-term AI engineering, backend engineering, and data systems portfolio project.

The Percy Jackson universe is the knowledge domain — chosen because it contains a large, richly interconnected set of entities (characters, gods, powers, quests, monsters, locations, books, prophecies) that is understandable, testable, and interesting to work with, while the underlying engineering techniques are intended to generalise to any structured/unstructured knowledge domain, including enterprise use cases.

---

## Why this project exists

1. **To build a flagship portfolio project** for graduate and junior roles in AI engineering, software engineering, machine learning engineering, backend engineering, and data engineering.
2. **To go deep rather than wide.** Many portfolio projects demonstrate that someone can call an LLM API. This project is explicitly intended to demonstrate genuine engineering ability across backend architecture, database engineering, retrieval systems, AI system design, evaluation, testing, and production practices — the kind of depth that survives a technical interview, not just a demo.
3. **To continue past coursework.** The original relational database was completed as coursework. Rather than treat that as finished, it's being used as a foundation to build a much larger, self-directed system.
4. **To build genuine capability**, not just a finished artifact. The process of building this — and being able to explain every decision in it — is treated as equally important as the end result.

---

## Target roles

This project is being built with the following target roles in mind:

- AI Engineer
- Software Engineer
- Machine Learning Engineer
- Backend Engineer
- Data Engineer

The engineering quality bar is set at: *strong enough to be credible for highly technical software engineering and quantitative development roles*, not just AI-adjacent roles.

---

## Engineering principles (non-negotiable)

These principles should be used to evaluate every proposed feature, not just referenced occasionally:

1. **This is not a CRUD app with an LLM attached.** Any AI feature added must be backed by genuine retrieval, grounding, or reasoning infrastructure — not a thin prompt wrapper around the database.
2. **Engineering depth over feature count.** A smaller number of well-tested, well-reasoned, well-documented components is preferred over a larger number of shallow ones.
3. **Every architectural decision must be defensible.** If a technology or pattern can't be justified against realistic alternatives in an interview setting, it shouldn't be in the project — or it needs an ADR explaining why it's there anyway.
4. **Evaluate, don't assume.** AI and retrieval functionality must be measured (accuracy, retrieval quality, hallucination rate, latency, cost) rather than judged by "it looks like it works."
5. **Security and correctness are built in, not bolted on.** Input validation, parameterised queries, and least-privilege access are expected from the start of any new feature, not retrofitted later.
6. **Do not add technology purely for resume keywords.** Every dependency and pattern should solve a real, stated problem in this project.
7. **Documentation is treated as an engineering artifact**, not an afterthought — this document set is part of the deliverable, not separate from it.

---

## Relationship to original coursework

The relational schema, initial FastAPI backend, SQLAlchemy models, SQL views, and stored procedures originate from a university Database Systems course (CMSC 4323). That foundation is being reviewed, corrected, tested, and extended as part of this project rather than treated as a finished, untouchable artifact — see `ENGINEERING_LOG.md` for the audit that established the current baseline state.

---

## How this documentation set fits together

| Document | Answers | Update frequency |
|---|---|---|
| `PROJECT_CONTEXT.md` (this file) | Why does this exist, and what are the non-negotiable principles? | Rarely |
| `ARCHITECTURE.md` | How does the system work, right now? | Whenever implementation changes |
| `ROADMAP.md` | What's the current phase and near-term priority? | Every planning session |
| `DEVELOPMENT_ROADMAP.md` | What's the full long-term plan, in detail? | Rarely — major replanning only |
| `ENGINEERING_LOG.md` | What did I do, decide, and learn, session by session? | Every working session |
| `docs/adr/` (planned) | Why was a specific significant decision made? | One new file per major decision |

---

## Open items / to confirm

- [ ] Contact/profile links to include here (or intentionally omit)
- [ ] License decision (see engineering log entry for 2026-08-06 for tradeoffs discussed)