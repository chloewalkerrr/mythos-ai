# MythosAI — Architecture (Current State)

**Last updated:** 2026-08-08
**Scope:** This document describes the system **as it currently exists in code**. It does not describe planned or future architecture — see `ROADMAP.md` and `DEVELOPMENT_ROADMAP.md` for that. If something in this document becomes inaccurate after a code change, update this file in the same change, not later.

---

## 1. System Overview

MythosAI is currently a single-layer backend system: a FastAPI REST API sitting directly on a SQLAlchemy ORM layer, backed by a relational database. There is no frontend, no authentication layer, no AI/LLM functionality, and no deployment infrastructure in the codebase at this time.

Client (Swagger UI / HTTP client)
│
▼
FastAPI application (api/main.py + routers)
│
▼
SQLAlchemy ORM session (models/base.py::get_db)
│
▼
MariaDB / MySQL (development) | SQLite in-memory (automated tests)

---

## 2. Components

### 2.1 API Layer

- Framework: FastAPI, entrypoint `api/main.py`.
- Routing is split into feature-based `APIRouter` modules: `api/characters.py`, `api/gods.py`, `api/quests.py`, each included into the main app.
- `api/main.py` additionally defines cross-entity join endpoints and endpoints backed by raw SQL (views, stored procedures) directly, rather than through a router module.
- Request validation and response shaping for the `Character` entity uses Pydantic schemas (`schemas/character.py`: `CharacterCreate`, `CharacterUpdate`, `CharacterResponse`).
- No other entity currently has dedicated Pydantic schemas; the `God` and `Quest` routers return raw SQLAlchemy ORM instances without a declared `response_model`.

### 2.2 Data / ORM Layer

- ORM: SQLAlchemy, using the classic `declarative_base()` pattern.
- Models are split across `models/character.py`, `models/god.py`, and `models/all_models.py` (Cabin, Monster, Location, Quest, Book, Weapon, Prophecy, Power, and the junction tables CharacterPower, QuestParticipant, QuestMonster).
- `models/base.py` builds the database connection string from a validated `Settings` instance (`models/config.py`, backed by `pydantic-settings`), exposes `engine`, `SessionLocal`, and a `get_db()` FastAPI dependency that yields a session and guarantees closure via `finally`.
- Table creation is currently performed via `Base.metadata.create_all()` (`scripts/create_tables.py`) — there is no migration tool (e.g. Alembic) in use, so schema changes are not versioned or reversible.

### 2.3 Database

- Target database: MariaDB/MySQL in development, connected via PyMySQL.
- 13 tables total, normalised, with explicit foreign keys and `ondelete` behaviour (`CASCADE` on junction tables, `SET NULL` on optional parent references).
- `CheckConstraint`s enforce numeric ranges on several columns (character age, quest difficulty, power level, cabin number, threat level values, quest status values).
- Indexes are defined on frequently-filtered columns (e.g. character name, parent god, quest status).
- Two enum classes are declared (`QuestStatus`, `MonsterThreatLevel` in `models/all_models.py`) but are not currently attached to any column — the equivalent validation is instead enforced via string-based `CheckConstraint`s.

### 2.4 Raw SQL: Views and Stored Procedures

- `sql/views.sql` defines three views: `character_power_summary`, `quest_statistics`, `active_demigods`. Only `character_power_summary` is currently queried by an API endpoint (`GET /views/character-summary` in `api/main.py`).
- `sql/procedures.sql` defines three stored procedures. Only the first, `GetCharactersByGodParent`, appears syntactically valid and is the only one called from the API (`GET /procedures/god-children/{god_name}`). The other two (`GetQuestDetails`, `UpdateCharacterStatus`) are missing their `CREATE PROCEDURE` statements and are not callable as written — this is tracked as a known defect, not a design choice.
- Where user input reaches raw SQL, it is passed via SQLAlchemy's parameterised `text()` binding (dictionary parameters), not string interpolation.

### 2.5 Testing

- Framework: pytest, with FastAPI's `TestClient`.
- `tests/conftest.py` defines an isolated in-memory SQLite database (`sqlite://` with `StaticPool`), created and torn down per test via the `db_session` fixture, and overrides the `get_db` dependency so the API under test never touches the development database.
- A `sample_data` fixture seeds a minimal, consistent dataset (one god, one character, one power, one book, one quest, one participant) for tests that need existing data.
- `tests/test_api.py` contains 17 tests covering API docs availability, OpenAPI schema generation, character CRUD, validation errors, 404 handling, god-child relationships, and join endpoints.

### 2.6 CI/CD

- `.github/workflows/ci.yml` runs on pushes and pull requests targeting `dev` and `main`.
- Pipeline: install dependencies from `requirements.txt` → Ruff lint (`ruff check .`) → Ruff format check (`ruff format . --check`) → `pytest`.
- There is no build, containerisation, or deployment step — CI currently validates code quality and correctness only.

---

## 3. Request Lifecycle (traced example)

**`GET /characters/{id}`:**

1. FastAPI routes the request to `get_character` in `api/characters.py`.
2. The `get_db` dependency (`models/base.py`) opens a new SQLAlchemy session.
3. The handler queries `Character` by primary key via the ORM.
4. If no row is found, an `HTTPException(404, "Not found")` is raised.
5. If found, the ORM object is serialised through the `CharacterResponse` Pydantic model (declared via `response_model=CharacterResponse`), which filters and types the returned fields.
6. FastAPI serialises the Pydantic model to JSON and returns it.
7. The `get_db` generator's `finally` block closes the session after the response is generated.

**Join endpoints** (e.g. `GET /characters/{id}/quests` in `api/main.py`) follow the same session lifecycle but build the response as plain dictionaries from tuple query results, rather than via a Pydantic model — there is currently no declared response contract for these endpoints.

**View/procedure endpoints** execute raw SQL via `db.execute(text(...))` and convert `RowMapping` results to dictionaries directly.

---

## 4. Data Model Summary

13 tables, grouped by role:

- **Core entities:** `characters`, `gods`, `cabins`, `quests`, `books`, `locations`, `monsters`, `weapons`, `powers`, `prophecies`
- **Junction (many-to-many) tables:** `character_powers`, `quest_participants`, `quest_monsters`

Key relationships:
- A `Character` optionally belongs to one `God` (parent) and one `Cabin`.
- A `Character` has many `Weapon`s, and many-to-many relationships to `Power` (via `character_powers`) and `Quest` (via `quest_participants`).
- A `Quest` optionally references a `Book`, a `Prophecy`, a start `Location`, and an end `Location`, and has many-to-many relationships to `Character` and `Monster` (via `quest_monsters`).

A full entity-relationship diagram is not currently maintained as a separate artifact — see the "Suggested Improvements" note in the engineering log regarding a future `DATA_MODEL.md`.

---

## 5. Configuration and Environment

- Configuration is now validated at startup via `pydantic-settings` (`models/config.py`): a `Settings(BaseSettings)` class reads from a `.env` file (`SettingsConfigDict(env_file=".env", extra="ignore")`), replacing the previous raw `os.getenv()` + `python-dotenv` approach.
- `db_user` and `db_name` are declared as required fields (no default) — if either is missing, `Settings()` raises a `pydantic_core.ValidationError` immediately at import time, naming the specific missing field(s), rather than silently building a broken connection string. `db_password`, `db_host`, and `db_port` have defaults (`""`, `"localhost"`, `"3306"`) and remain optional. `db_port` is intentionally typed as `str`, not `int` — its only use in the codebase is string interpolation into a connection URL, never numeric operations.
- `extra="ignore"` is set because `.env.example` reserves additional keys (`API_HOST`, `API_PORT`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) not yet modeled as `Settings` fields and not currently referenced anywhere else in the codebase; without this, Pydantic's default behavior would reject the file for containing undeclared keys.
- `models/base.py` builds `DATABASE_URL` from the validated `settings` instance rather than raw environment reads.
- `.env` remains excluded from version control via `.gitignore`; `.env.example` documents the required variables without real values.
- **Known gap:** `db_password` is currently a plain `str` field, not Pydantic's `SecretStr` — meaning a real password, if one existed, could be exposed in full via `print(settings)` or an unguarded log statement. Deferred as of 2026-08-08; low risk today since local dev uses no password, but a genuine gap the moment a real secret is used.
- **Known gap:** the fail-fast validation behavior itself (that `Settings()` correctly raises when a required field is missing) has only been verified manually, not by an automated test.

---

Sure — here's the full content of each. Copy each block exactly as-is into the corresponding file.

PROJECT_CONTEXT.md
markdown
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
ARCHITECTURE.md
markdown
# MythosAI — Architecture (Current State)

**Last updated:** 2026-08-08
**Scope:** This document describes the system **as it currently exists in code**. It does not describe planned or future architecture — see `ROADMAP.md` and `DEVELOPMENT_ROADMAP.md` for that. If something in this document becomes inaccurate after a code change, update this file in the same change, not later.

---

## 1. System Overview

MythosAI is currently a single-layer backend system: a FastAPI REST API sitting directly on a SQLAlchemy ORM layer, backed by a relational database. There is no frontend, no authentication layer, no AI/LLM functionality, and no deployment infrastructure in the codebase at this time.

Client (Swagger UI / HTTP client)
│
▼
FastAPI application (api/main.py + routers)
│
▼
SQLAlchemy ORM session (models/base.py::get_db)
│
▼
MariaDB / MySQL (development) | SQLite in-memory (automated tests)


---

## 2. Components

### 2.1 API Layer

- Framework: FastAPI, entrypoint `api/main.py`.
- Routing is split into feature-based `APIRouter` modules: `api/characters.py`, `api/gods.py`, `api/quests.py`, each included into the main app.
- `api/main.py` additionally defines cross-entity join endpoints and endpoints backed by raw SQL (views, stored procedures) directly, rather than through a router module.
- Request validation and response shaping for the `Character` entity uses Pydantic schemas (`schemas/character.py`: `CharacterCreate`, `CharacterUpdate`, `CharacterResponse`).
- No other entity currently has dedicated Pydantic schemas; the `God` and `Quest` routers return raw SQLAlchemy ORM instances without a declared `response_model`.

### 2.2 Data / ORM Layer

- ORM: SQLAlchemy, using the classic `declarative_base()` pattern.
- Models are split across `models/character.py`, `models/god.py`, and `models/all_models.py` (Cabin, Monster, Location, Quest, Book, Weapon, Prophecy, Power, and the junction tables CharacterPower, QuestParticipant, QuestMonster).
- `models/base.py` builds the database connection string from a validated `Settings` instance (`models/config.py`, backed by `pydantic-settings`), exposes `engine`, `SessionLocal`, and a `get_db()` FastAPI dependency that yields a session and guarantees closure via `finally`.
- Table creation is currently performed via `Base.metadata.create_all()` (`scripts/create_tables.py`) — there is no migration tool (e.g. Alembic) in use, so schema changes are not versioned or reversible.

### 2.3 Database

- Target database: MariaDB/MySQL in development, connected via PyMySQL.
- 13 tables total, normalised, with explicit foreign keys and `ondelete` behaviour (`CASCADE` on junction tables, `SET NULL` on optional parent references).
- `CheckConstraint`s enforce numeric ranges on several columns (character age, quest difficulty, power level, cabin number, threat level values, quest status values).
- Indexes are defined on frequently-filtered columns (e.g. character name, parent god, quest status).
- Two enum classes are declared (`QuestStatus`, `MonsterThreatLevel` in `models/all_models.py`) but are not currently attached to any column — the equivalent validation is instead enforced via string-based `CheckConstraint`s.

### 2.4 Raw SQL: Views and Stored Procedures

- `sql/views.sql` defines three views: `character_power_summary`, `quest_statistics`, `active_demigods`. Only `character_power_summary` is currently queried by an API endpoint (`GET /views/character-summary` in `api/main.py`).
- `sql/procedures.sql` defines three stored procedures. Only the first, `GetCharactersByGodParent`, appears syntactically valid and is the only one called from the API (`GET /procedures/god-children/{god_name}`). The other two (`GetQuestDetails`, `UpdateCharacterStatus`) are missing their `CREATE PROCEDURE` statements and are not callable as written — this is tracked as a known defect, not a design choice.
- Where user input reaches raw SQL, it is passed via SQLAlchemy's parameterised `text()` binding (dictionary parameters), not string interpolation.

### 2.5 Testing

- Framework: pytest, with FastAPI's `TestClient`.
- `tests/conftest.py` defines an isolated in-memory SQLite database (`sqlite://` with `StaticPool`), created and torn down per test via the `db_session` fixture, and overrides the `get_db` dependency so the API under test never touches the development database.
- A `sample_data` fixture seeds a minimal, consistent dataset (one god, one character, one power, one book, one quest, one participant) for tests that need existing data.
- `tests/test_api.py` contains 17 tests covering API docs availability, OpenAPI schema generation, character CRUD, validation errors, 404 handling, god-child relationships, and join endpoints.

### 2.6 CI/CD

- `.github/workflows/ci.yml` runs on pushes and pull requests targeting `dev` and `main`.
- Pipeline: install dependencies from `requirements.txt` → Ruff lint (`ruff check .`) → Ruff format check (`ruff format . --check`) → `pytest`.
- There is no build, containerisation, or deployment step — CI currently validates code quality and correctness only.

---

## 3. Request Lifecycle (traced example)

**`GET /characters/{id}`:**

1. FastAPI routes the request to `get_character` in `api/characters.py`.
2. The `get_db` dependency (`models/base.py`) opens a new SQLAlchemy session.
3. The handler queries `Character` by primary key via the ORM.
4. If no row is found, an `HTTPException(404, "Not found")` is raised.
5. If found, the ORM object is serialised through the `CharacterResponse` Pydantic model (declared via `response_model=CharacterResponse`), which filters and types the returned fields.
6. FastAPI serialises the Pydantic model to JSON and returns it.
7. The `get_db` generator's `finally` block closes the session after the response is generated.

**Join endpoints** (e.g. `GET /characters/{id}/quests` in `api/main.py`) follow the same session lifecycle but build the response as plain dictionaries from tuple query results, rather than via a Pydantic model — there is currently no declared response contract for these endpoints.

**View/procedure endpoints** execute raw SQL via `db.execute(text(...))` and convert `RowMapping` results to dictionaries directly.

---

## 4. Data Model Summary

13 tables, grouped by role:

- **Core entities:** `characters`, `gods`, `cabins`, `quests`, `books`, `locations`, `monsters`, `weapons`, `powers`, `prophecies`
- **Junction (many-to-many) tables:** `character_powers`, `quest_participants`, `quest_monsters`

Key relationships:
- A `Character` optionally belongs to one `God` (parent) and one `Cabin`.
- A `Character` has many `Weapon`s, and many-to-many relationships to `Power` (via `character_powers`) and `Quest` (via `quest_participants`).
- A `Quest` optionally references a `Book`, a `Prophecy`, a start `Location`, and an end `Location`, and has many-to-many relationships to `Character` and `Monster` (via `quest_monsters`).

A full entity-relationship diagram is not currently maintained as a separate artifact — see the "Suggested Improvements" note in the engineering log regarding a future `DATA_MODEL.md`.

---

## 5. Configuration and Environment

- Configuration is now validated at startup via `pydantic-settings` (`models/config.py`): a `Settings(BaseSettings)` class reads from a `.env` file (`SettingsConfigDict(env_file=".env", extra="ignore")`), replacing the previous raw `os.getenv()` + `python-dotenv` approach.
- `db_user` and `db_name` are declared as required fields (no default) — if either is missing, `Settings()` raises a `pydantic_core.ValidationError` immediately at import time, naming the specific missing field(s), rather than silently building a broken connection string. `db_password`, `db_host`, and `db_port` have defaults (`""`, `"localhost"`, `"3306"`) and remain optional. `db_port` is intentionally typed as `str`, not `int` — its only use in the codebase is string interpolation into a connection URL, never numeric operations.
- `extra="ignore"` is set because `.env.example` reserves additional keys (`API_HOST`, `API_PORT`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) not yet modeled as `Settings` fields and not currently referenced anywhere else in the codebase; without this, Pydantic's default behavior would reject the file for containing undeclared keys.
- `models/base.py` builds `DATABASE_URL` from the validated `settings` instance rather than raw environment reads.
- `.env` remains excluded from version control via `.gitignore`; `.env.example` documents the required variables without real values.
- **Known gap:** `db_password` is currently a plain `str` field, not Pydantic's `SecretStr` — meaning a real password, if one existed, could be exposed in full via `print(settings)` or an unguarded log statement. Deferred as of 2026-08-08; low risk today since local dev uses no password, but a genuine gap the moment a real secret is used.
- **Known gap:** the fail-fast validation behavior itself (that `Settings()` correctly raises when a required field is missing) has only been verified manually, not by an automated test.

---

## 6. Known Limitations (as of this document's last update)

These are stated explicitly so this document stays honest about the current system rather than implying more maturity than exists:

- No authentication or authorization on any endpoint.
- No CORS configuration.
- No rate limiting, structured logging, or observability.
- No database migration tooling (schema versioning is all-or-nothing via `create_all()`).
- Only the `Character` entity has full CRUD and a declared Pydantic response contract; 10 of 13 entities have no API exposure at all.
- Two of three stored procedures in `sql/procedures.sql` are not valid, callable SQL.
- Two of three SQL views are defined but unused by any endpoint.

---

## 7. Explicitly Out of Scope Right Now

The following exist only as planning content in `DEVELOPMENT_ROADMAP.md` and must not be assumed to be implemented: natural-language-to-SQL, knowledge graph, retrieval-augmented generation, vector search, agentic tool use, open-weight model integration, machine learning/recommendation features, a formal evaluation framework, containerisation, and cloud deployment.