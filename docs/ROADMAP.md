# MythosAI — Roadmap

**Last updated:** 2026-08-08

## Purpose of this document

This is a short, current-state roadmap: what phase the project is in, what's genuinely done, and what the near-term priority is. It is meant to be read in under two minutes.

For the full 14-phase long-term plan with detailed task breakdowns, architecture diagrams, and evaluation criteria per phase, see `DEVELOPMENT_ROADMAP.md`. This document should not duplicate that detail — it should only summarise it and point to it.

**Update policy:** update this document at the start and end of each planning session, or whenever the current phase or immediate priority changes. It should never go stale for long — if it hasn't been touched in a while, that's a signal to revisit it, not evidence nothing changed.

---

## Current Phase

**Phase 1 — Core Platform** (partially complete)

Per `DEVELOPMENT_ROADMAP.md` §4, Phase 1's completion criterion is: *a user can run MythosAI locally and browse, search and explore the database through a working frontend without directly interacting with SQL or Swagger.* This criterion is **not yet met** — there is no frontend, and the API surface itself is incomplete.

---

## Status Snapshot (updated 2026-08-08)

**Done:**
- Normalised 13-table relational schema with constraints and indexes
- SQLAlchemy ORM models for all 13 tables
- FastAPI backend with modular routers
- Full CRUD (with Pydantic validation) for the `Character` entity
- One working SQL view and one working stored procedure, each exposed via an endpoint
- 17 automated backend tests, isolated test database, CI pipeline (lint, format, test)
- `.gitattributes` added; `requirements.txt` normalized from UTF-16 to UTF-8
- Fail-fast configuration validation via `pydantic-settings` (`models/config.py`) — `db_user`/`db_name` are now required, validated fields; `models/base.py` builds `DATABASE_URL` from validated `settings` instead of raw `os.getenv()`
- Fixed both broken stored procedures; verified working against real database
- Found and fixed sql/views.sql drift from the real database; wired up the two
  previously-unused views as new API endpoints
  - Alembic set up for database migrations; live database schema now matches the models (including the Session 2 enum changes)
  - God: full CRUD, typed schemas, tested (reference pattern for remaining entities)
  - Cabin and Location: full CRUD, typed schemas, tested (100% coverage on both)

**Not yet done:**
- CRUD for the other 12 entities (only `Character` has full CRUD)
- Pydantic response schemas for entities other than `Character`
- Two of three stored procedures are broken (invalid SQL) and need fixing or rewriting
- Two of three SQL views are unused by any endpoint
- Database migration tooling (Alembic or equivalent)
- Frontend of any kind
- Authentication, CORS, rate limiting, structured logging
- `SecretStr` for `db_password` (currently a plain `str` — could be printed/logged in full)
- Automated test proving the fail-fast validation behavior itself (currently only manually verified)
- `pytest-cov`, `pre-commit`, `docs/adr/` folder (originally scoped for Session 1, deferred to "Session 1b")

---

## Immediate Next Priority

**Milestone: Complete and Consistent Core Data/API Layer.** Full CRUD, typed request/response schemas, and consistent validation across all 13 entities, plus resolution of the two known SQL defects (`sql/procedures.sql`, `sql/views.sql`). This was chosen because it's the one candidate every later phase (frontend, NL-to-SQL, knowledge graph) directly depends on. Full candidate comparison and reasoning: see `ENGINEERING_LOG.md`, 2026-08-06.

**Next session ("Session 1b"):** finish the originally-scoped Session 1 tooling — `pytest-cov`, `pre-commit`, `docs/adr/` — and/or close the two items deferred from today (`SecretStr` for `db_password`, an automated fail-fast validation test). `chore/dev-tooling` merged into `dev` on 2026-08-08 (PR included three rounds of CI-driven fixes — see `ENGINEERING_LOG.md`, 2026-08-08, "PR review and CI debugging" — worth reading before Session 1b, since it directly motivates adding `pre-commit`).

## Technology Decision Register

Maintained here as a living record of every substantial tool, library, or practice considered for MythosAI. Nothing is adopted purely to make the stack look larger — each entry states the real problem it solves and when it should be revisited.

| Technology / Practice | Status | Problem it addresses | Reason for decision | Revisit when |
|---|---|---|---|---|
| `pydantic-settings` | **Adopted & implemented** (2026-08-08) | No startup validation of required env vars (`models/base.py` silently builds a broken connection string) | Fixes a real defect found in the repository audit; reuses the Pydantic pattern already in the codebase | If config needs grow complex enough to need per-environment profiles |
| Architecture Decision Records (ADRs) | Adopted (decision made; `docs/adr/` folder not yet created) | Reasoning behind significant decisions gets lost over time | First genuine ADR-worthy decision (validation strategy) is imminent | N/A — ongoing practice |
| `pytest-cov` | Adopted (decision made; not yet installed/configured — planned for Session 1b) | Risk of an entity being silently under-tested as CRUD is replicated across 13 entities | Test suite is about to scale ~12x; mechanical coverage check is more reliable than manual review at that scale | Once a meaningful threshold can be justified, consider gating CI on it |
| `pre-commit` (Ruff hooks) | Adopted (decision made; not yet installed/configured — planned for Session 1b) | Lint/format issues currently caught only in CI, after push | Repetitive scaffolding work in Milestone A makes local fast-feedback worthwhile | N/A — low-cost, ongoing |
| Alembic (migrations) | Deferred | Schema changes currently unversioned (`create_all()` only) | No schema change is happening in Milestone A — only new endpoints/schemas | Start of Milestone B (next schema-changing work) |
| Docker / containerisation | Deferred | No reproducible runtime environment | Deployment target undecided; containerising now risks redoing it later | Once a deployment target is chosen |
| Cloud deployment | Deferred | No hosted environment | Same as above | Same as above |
| Structured logging / observability | Deferred | No request tracing or multi-stage pipeline yet | Nothing complex enough yet to need trace correlation | Once an AI/retrieval pipeline (Phase 2+) or hosted deployment exists |
| Authentication / rate limiting | Deferred | All endpoints are currently unauthenticated | API surface isn't complete yet; adding auth now means re-testing every endpoint twice | Before any public deployment |
| AI/retrieval evaluation framework | Deferred | N/A — no AI functionality exists yet | Introducing evaluation tooling before there's anything to evaluate is premature complexity | Start of Phase 2 |
| `mypy` / static typing | Deferred | Dynamic typing risk in a growing codebase | Classic SQLAlchemy `declarative_base()` type-checks poorly without extra stubs | If/when migrating to SQLAlchemy 2.0's typed declarative style |
| `factory_boy` / test data factories | Deferred | Manual fixture construction in `conftest.py` could become repetitive at scale | Not yet a real pain point with only a few entities fixtured | If fixture duplication becomes noticeable, watch during Sessions 5–8 |

**Update policy:** update this table whenever a technology's status changes (adopted, evaluating → adopted/deferred, or a revisit trigger fires) — not on every code change.

---

## Long-Term Phase Index

Full detail for every phase lives in `DEVELOPMENT_ROADMAP.md`. Summary only:

| Phase | Focus | Status |
|---|---|---|
| 1 | Core relational platform, FastAPI backend, frontend explorer | In progress |
| 2 | Natural-language-to-SQL querying | Not started |
| 3 | Knowledge graph over the relational data | Not started |
| 4 | Retrieval-Augmented Generation over unstructured text | Not started |
| 5 | Hybrid retrieval/reasoning router | Not started |
| 6 | Agentic multi-step tool use | Not started |
| 7 | Open-weight model experimentation | Not started |
| 8 | Machine learning / recommendation system | Not started |
| 9 | Formal AI evaluation framework | Not started |
| 10 | Security and AI guardrails | Not started |
| 11 | Production engineering (Docker, CI/CD, cloud deployment) | Not started |
| 12 | Observability | Not started |
| 13 | Fine-tuning / small language model research | Not started |
| 14 | Model Context Protocol exposure | Not started |

---

## Relationship to Other Documents

- `PROJECT_CONTEXT.md` — why this project exists and what principles govern decisions
- `ARCHITECTURE.md` — how the system works today, in detail
- `DEVELOPMENT_ROADMAP.md` — the full long-term plan this document summarises
- `ENGINEERING_LOG.md` — the session-by-session record of how the roadmap is actually being executed