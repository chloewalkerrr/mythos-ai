# MythosAI — Engineering Log

This is a chronological, append-only journal of working sessions on MythosAI. It exists to capture reasoning and learning that would otherwise be lost — the "why" behind decisions, not just the "what" that's visible in the git history.

**Rules for this document:**
- Entries are appended in date order and never rewritten or deleted, even if a later decision reverses an earlier one — add a new entry that says so instead.
- This log starts from 2026-08-06. Everything before that date is treated as inherited baseline state (see `PROJECT_CONTEXT.md`) and is not reconstructed here, except where explicitly verifiable from Git history.
- Every entry uses the same template, filled in honestly, including when something didn't go well.

**Template:**
YYYY-MM-DD — Short title

Objective:
What I set out to do this session.

Work completed:
What was actually done.

Engineering decisions:
Any decision made, with the reasoning and alternatives considered.

Technical concepts learned:
Anything new understood this session — even if minor.

Challenges encountered:
What was difficult, confusing, or went wrong.

Next steps:
What follows from this session.
---

## 2026-08-06 — Repository audit and documentation foundation

**Objective:**
Perform a complete, honest audit of the existing MythosAI repository (inherited from prior coursework) before making any further changes, and establish a long-term documentation structure to support ongoing development as a portfolio project.

**Work completed:**
- Full repository audit covering: overall architecture, frontend/backend/database/API/AI component inventory, data flow tracing, completeness assessment, technical debt, bugs, security concerns, and structural recommendations.
- Confirmed the current system is a FastAPI + SQLAlchemy backend over a 13-table relational schema (MariaDB/MySQL in dev, SQLite in tests), with no frontend, no authentication, and no AI/LLM functionality implemented yet — despite the project's long-term AI-engineering vision.
- Identified that only the `Character` entity has full CRUD and a Pydantic response contract; 10 of 13 entities have no API exposure.
- Identified that 2 of 3 stored procedures in `sql/procedures.sql` are syntactically invalid (missing `CREATE PROCEDURE` statements) and are not callable.
- Identified that 2 of 3 SQL views are defined but never queried by any endpoint.
- Established a four-document documentation structure (`PROJECT_CONTEXT.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `ENGINEERING_LOG.md`) inside `docs/`, alongside the existing `DEVELOPMENT_ROADMAP.md`, and drafted the first version of each.

**Engineering decisions:**
- **Kept `DEVELOPMENT_ROADMAP.md` as-is rather than merging it into a new roadmap document.** Reasoning: it serves a different purpose (comprehensive, rarely-changing long-form plan) than the new `ROADMAP.md` (short, frequently-updated current-status summary). Merging them would force either constant edits to a long document or a loss of the quick-orientation view. Alternative considered: replacing `DEVELOPMENT_ROADMAP.md` entirely — rejected because its detail is still accurate and useful as a reference.
- **`ARCHITECTURE.md` documents only the current system state, with all future/target architecture kept in `ROADMAP.md`/`DEVELOPMENT_ROADMAP.md`.** Reasoning: mixing "what is" and "what will be" in one document is a common source of confusion, and misrepresents project maturity to a reader (e.g. an interviewer).
- **`ENGINEERING_LOG.md` starts fresh from today rather than reconstructing history.** Reasoning: the prior development history isn't reliably reconstructable from the repository alone without risking fabricated or inaccurate reasoning being presented as fact; only Git-history-verifiable events would be trustworthy, and none were used to backfill entries in this pass.
- **Deferred creating `adr/`, `SECURITY.md`, `TESTING_STRATEGY.md`, `EVALUATION.md`, and `DATA_MODEL.md`** rather than scaffolding empty files now. Reasoning: these are valuable but should be created when there's real content to put in them, not as placeholders.
- **Left `ROADMAP.md`'s "immediate next priority" section explicitly unfilled**, pending a decision on what to prioritise next, rather than guessing at a priority.

**Technical concepts learned / reinforced:**
- The distinction between an **Architecture Decision Record** (a permanent, decision-indexed justification) and a chronological engineering log (a narrative journal) — both are useful, but for different retrieval purposes: "why did we choose X" vs. "what happened during this session."
- Why `DROP PROCEDURE IF EXISTS <name>(...)` with a parameter list is invalid MariaDB/MySQL syntax — `DROP PROCEDURE` only ever takes a bare procedure name, since a procedure name alone is enough to identify it for dropping (MySQL doesn't support procedure overloading by signature the way some languages support function overloading).
- Why returning raw SQLAlchemy ORM objects without a `response_model` is a fragile pattern in FastAPI even when it currently "works" — there's no declared contract, and lazy-loaded relationships accessed after session teardown can raise errors that only surface once a particular relationship path is hit.

**Challenges encountered:**
None significant this session — this was primarily an inspection and documentation session rather than an implementation one.

**Next steps:**
- Decide and record the immediate development priority in `ROADMAP.md` (candidates surfaced in the audit: fix the two broken stored procedures, extend CRUD coverage to remaining entities, or introduce Alembic for migrations).
- Decide on a license (MIT vs. no license) — tradeoffs discussed but not yet resolved.
- Confirm whether any genuine reasoning exists for early technology choices (e.g. MariaDB over PostgreSQL) worth capturing as the project's first ADR, or whether that decision predates any deliberate tradeoff analysis.

---

## 2026-08-06 — Milestone selection and technology decision register

**Objective:**
Decide the next engineering milestone (following on from the audit) and establish a disciplined process for evaluating any tool or practice before adopting it, so the project gains genuine professional-practice exposure without artificial complexity.

**Work completed:**
- Compared six candidate milestones (complete/consistent core data-API layer, Alembic migrations, SQL layer + safe query execution pattern, testing strategy expansion, config/observability hardening, containerisation) against the criterion: does it reduce risk or add capability that later AI phases will directly depend on.
- Selected **Milestone: Complete and Consistent Core Data/API Layer** as the next milestone, with Alembic and a safe SQL execution layer explicitly queued as the two milestones after it.
- Established a technology decision register in `ROADMAP.md`, evaluated against a fixed 7-point framework (real problem solved, professional usage context, appropriateness at current scale, simpler alternatives, tradeoffs/operational cost, adopt-now-vs-defer, and the interview-explainable learning outcome) for every tool considered.
- Adopted four items for Milestone A: `pydantic-settings` (typed, fail-fast configuration), Architecture Decision Records as a formal practice, `pytest-cov` (coverage reporting, not yet a CI gate), and `pre-commit` (local Ruff hooks).
- Explicitly deferred, with stated revisit triggers: Alembic, Docker/containerisation, cloud deployment, structured logging/observability, authentication/rate limiting, AI/retrieval evaluation frameworks, `mypy`, and test data factories (`factory_boy`).
- Revised the Milestone A task sequence from 9 to 10 sessions, adding a dedicated tooling-setup session (Session 1) ahead of the validation-strategy decision (Session 2), and mapped which sessions introduce new tools vs. which are deliberately tool-free repetitions of an established pattern (Sessions 5–8).

**Engineering decisions:**
- **`pydantic-settings` adopted now rather than deferred.** Reasoning: it directly fixes a defect already identified in the audit (no startup validation of required env vars in `models/base.py`), and reuses a pattern (Pydantic models) already present in the codebase, so the learning cost is marginal, not new.
- **ADRs adopted as a practice, not a tool.** Reasoning: zero infrastructure cost (a markdown convention), and the validation-strategy decision queued for Session 2 is the project's first genuine ADR-worthy moment — better to establish the practice before that decision is made than retrofit it after.
- **`pytest-cov` adopted for reporting only, explicitly not as a CI-blocking gate yet.** Reasoning: a coverage threshold chosen now would be arbitrary; better to observe real coverage as the suite scales across 13 entities and set a threshold once there's evidence for what's meaningful.
- **`mypy` deferred rather than adopted**, despite being a common professional practice. Reasoning: the codebase's classic SQLAlchemy `declarative_base()` style type-checks poorly without additional stub packages — adopting it now would mean fighting the tool rather than benefiting from it. Flagged as a live open question tied to a possible future SQLAlchemy 2.0 migration, not a closed decision.
- **Docker, cloud deployment, auth, and observability all deferred**, each with an explicit revisit trigger tied to a real future event (deployment target chosen, Phase 2 beginning, public deployment) rather than a vague "later."

**Technical concepts learned / reinforced:**
- The distinction between a coverage percentage as a "floor-finder" (catches obviously untested code) versus a genuine quality metric — and why gating CI on an arbitrary threshold before that threshold means something is a common but avoidable mistake.
- Why local pre-commit hooks and CI checks are complementary, not redundant: local hooks optimise for fast feedback loop, CI is the authoritative, unavoidable gate.
- The practical reason SQLAlchemy's classic declarative style resists clean static type checking, and why that's a genuine (not hypothetical) blocker to adopting `mypy` today.

**Challenges encountered:**
None significant — this was a planning and documentation session.

**Next steps:**
- Begin Session 1 of Milestone A (tooling and workflow foundation: `pydantic-settings`, `pytest-cov`, `pre-commit`, ADR template/folder) when ready to start implementation.
- Revisit the license decision (still open from the prior session).

---

## 2026-08-08 — Repository cleanup: line endings and requirements.txt encoding

**Objective:**
Before beginning Session 1 implementation, verify the repository's actual working-tree state, resolve a suspected line-ending inconsistency, and get onto a clean, correctly-branched starting point.

**Work completed:**
- Confirmed via `git status` that the local working tree was already clean — the CRLF diff observed during an earlier zip-based inspection was an artifact of the upload/extraction process, not a real uncommitted change in the repository.
- Confirmed `core.autocrlf=true` locally (a sensible per-machine Windows setting) but recognized it doesn't help other contributors or CI, since it isn't part of the repository itself.
- Verified `requirements.txt` was genuinely committed as UTF-16LE (confirmed via raw byte inspection: `\xff\xfe` BOM), not just an artifact of the earlier zip transfer.
- Added `.gitattributes` (`* text=auto` plus explicit rules for `.py`/`.md`/`.toml`/`.yml`/`.sql`/`.txt`) to enforce LF line endings at the repository level, independent of any individual contributor's local Git config.
- Converted `requirements.txt` from UTF-16 to UTF-8, LF line endings. Verified the conversion two independent ways: (1) sorted-line-list comparison between the old (`git show HEAD:requirements.txt`) and new file content — confirmed identical; (2) `python -m pip install --dry-run -r requirements.txt` — all 26 packages resolved correctly at their pinned versions.
- Switched to `dev`, ran `git pull origin dev` (which correctly caught a real incoming commit that a stale "up to date" status message would have missed), created a fresh `chore/dev-tooling` branch off current `dev`, and committed the two fixes there (`55715fb`).
- Discovered and worked around a broken `pip.exe` launcher (pointed at a stale path from before the project folder was renamed from `percy_jackson_db` to `mythos-ai`) — resolved by using `python -m pip` instead of the `pip` executable directly; noted as a pre-existing environment issue, not something today's changes caused.

**Engineering decisions:**
- Verified before discarding anything, rather than assuming the earlier zip-based inspection reflected the real repository state — it didn't, and proceeding without checking would have meant "fixing" a problem that didn't actually exist in the real repo.
- Chose `.gitattributes` over relying on `core.autocrlf`, since the former is repository-level and enforced identically for every clone/CI run, while the latter is a personal, per-machine setting.
- Committed the line-ending/encoding fix as its own scoped `chore:` commit, separate from the `pydantic-settings` work that followed, so each commit represents one coherent unit of change.

**Technical concepts learned:**
- The difference between a repository-level fix (`.gitattributes`) and a personal-machine setting (`core.autocrlf`), and why only the former is reliable for a multi-contributor or CI context.
- Why `git status`'s "up to date with origin/X" message reflects the last fetch, not the current remote state — and why `git pull` is the only way to actually verify currency.
- How a UTF-16 BOM (`\xff\xfe`) appears at the byte level, and why Git's diff tooling treats a file as "binary" when comparing across an encoding boundary like this.
- The value of verifying a mechanical change two different ways (content-equivalence and functional-equivalence) rather than trusting either check alone.

**Challenges encountered:**
- A broken `pip.exe` launcher, caused by an earlier project-folder rename, blocked the planned `pip install --dry-run` verification step. Diagnosed via the error message (which named a stale, non-existent path) and worked around with `python -m pip` rather than treating it as a blocker.

**Next steps:**
- Recreate the local venv fresh at some point to fix the underlying broken `pip.exe` launcher (not urgent — `python -m pip` remains a reliable workaround).
- Proceed to Session 1 implementation now that the working tree and branch are clean.

---

## 2026-08-08 — Fail-fast configuration validation with pydantic-settings

**Objective:**
Fix the fail-fast configuration gap identified in the repository audit: `models/base.py` built `DATABASE_URL` from unvalidated `os.getenv()` calls, silently producing a broken connection string (containing the literal text `"None"`) if `DB_USER` or `DB_NAME` was unset, rather than failing clearly at startup.

**Work completed:**
- Added `pydantic-settings==2.7.1` as a dependency.
- Created `models/config.py`: a `Settings(BaseSettings)` class with `db_user` and `db_name` as required fields (no default) and `db_password`/`db_host`/`db_port` as optional with sensible defaults, reading from `.env` via `SettingsConfigDict(env_file=".env", extra="ignore")`.
- Updated `models/base.py` to build `DATABASE_URL` from the `settings` instance instead of raw `os.getenv()` calls; removed the now-unnecessary `load_dotenv()` call and `os` import.
- Manually verified both the failure and success paths: commented out `DB_USER` in `.env` and confirmed `Settings()` raises a clear `pydantic_core.ValidationError` naming the missing field; restored it and confirmed `DATABASE_URL` builds correctly.
- Ran the full existing test suite (17 tests) after the change — all still pass.
- Committed as `7d02870` on `chore/dev-tooling`.

**Engineering decisions:**
- `Settings` placed in a new `models/config.py` rather than inside `models/base.py`, on the reasoning that "what config does this app need" and "how do we connect to the database" are different responsibilities (separation of concerns) — especially relevant since `.env` already reserves `API_HOST`/`API_PORT`/`OPENAI_API_KEY`/`ANTHROPIC_API_KEY`, none of which are database-related.
- `db_port` kept as `str`, not `int` — its only use is string interpolation into a URL; there is no numeric operation performed on it anywhere in the codebase, so `str` is the more honest type for its actual current usage.
- `extra="ignore"` set on the settings config, since `.env` contains keys (`API_HOST`, the LLM API keys) not yet modeled as `Settings` fields; without this, Pydantic's default behavior would reject the file for containing "unexpected" keys.
- Deferred wrapping `db_password` in `SecretStr` to a follow-up session, rather than folding it into this one — a deliberate scope decision, not an oversight, made explicitly rather than silently skipped.

**Technical concepts learned:**
- Fail-fast validation as a design principle, and the concrete cost of its absence (a bug surfacing far from its actual cause).
- `if`/`raise` as the fundamental building block of a validation check, before moving to a library that provides this built in.
- The distinction between `ValueError` (right type, unacceptable value) and `TypeError` (wrong type entirely).
- How to read a Python traceback bottom-up, and how to interpret a pydantic `ValidationError` message specifically (field name, reason, and the `input_value` it saw).
- Why `BaseSettings` (env-var-aware) differs from plain `BaseModel` (validates data handed to it directly) — the same library, applied to a different kind of input.
- Recognizing which parts of an existing implementation don't need to change during a refactor (the `if`/`else` password-branch logic in `base.py` was correct before and remained correct after, and rewriting it anyway would have been unnecessary churn).

**Challenges encountered:**
- Python syntax (`if`/`raise`, colon, indentation, import direction, class vs. instance) took several iterations to get right — expected and fine, this was the actual point of the exercise.
- A first draft of the `base.py` rewrite correctly added the new settings-based logic but left the old, now-unnecessary `load_dotenv()`/`os` import in place — a good reminder to do a final read-through specifically checking for "things I meant to remove" before considering a refactor done.

**Unresolved / deferred:**
- `db_password` is currently a plain `str` field. Deferred: wrap it in Pydantic's `SecretStr` so it can't be accidentally printed or logged in full (e.g. via `print(settings)` or an unguarded log statement). Low risk today (local dev DB has no real password), but a real gap the moment any real secret lands in `.env`.
- No automated test yet proves the fail-fast behavior itself (that `Settings()` raises when a required field is missing) — only manually verified this session. Should add a pytest test using `monkeypatch` to unset a required env var and assert `ValidationError` is raised.

**Next steps:**
- Add the missing fail-fast test (`monkeypatch`-based).
- Implement `SecretStr` for `db_password`.
- Continue with the originally-scoped rest of Session 1: `pytest-cov`, `pre-commit`, and establishing the `docs/adr/` folder — treat as "Session 1b."
---

## 2026-08-08 — PR review and CI debugging: chore/dev-tooling → dev

**Objective:**
Open a pull request for the accumulated `chore/dev-tooling` work (line-ending/encoding fix,
`pydantic-settings` implementation, documentation set) against `dev`, get it passing CI, and
merge it.

**Work completed:**
- Pushed `chore/dev-tooling` to GitHub and opened a PR against `dev`, with a description
  summarizing all three prior commits and their verification steps.
- CI failed on first push with a Ruff linting error (`I001`, import-block sorting): local
  testing (pytest, manual imports) never runs Ruff, so this had never been checked locally.
  Fixed via `ruff check --fix`; verified clean with a follow-up `ruff check .`.
- CI failed again with a *different* Ruff error — the separate `ruff format . --check` step
  (blank-line spacing), a distinct tool from the linter. Fixed via `ruff format .`.
- Adopted a new habit at this point: run all three CI steps locally (`ruff check .`,
  `ruff format . --check`, `python -m pytest`) before every push, rather than pushing and
  waiting for CI to report issues one at a time.
- CI failed a third time, differently: `pytest` failed during collection with a
  `pydantic_core.ValidationError` — `db_user`/`db_name` "required, missing" — because
  GitHub's CI runner has no `.env` file (correctly never committed, per `.gitignore`), so
  `Settings()` found no configuration at all when the test suite imported the app.
- Diagnosed this as expected, correct behavior of the fail-fast validation built earlier
  this session — not a bug in that code — combined with a real, separate gap: CI had never
  been given its own configuration. Considered three options (fake `.env` values, making
  `Settings()` lazy/deferred, or CI-scoped environment variables in `ci.yml`) and chose the
  third: added `DB_USER`/`DB_NAME` as step-scoped `env:` values on the "Run tests" step.
- Verified the fix locally with a genuine test (not just a plausible-looking one): renamed
  `.env` out of the way entirely, set only the two environment variables, and confirmed the
  full test suite still passed 17/17 with no `.env` file present at all — then restored
  `.env`.
- Pushed the fix; CI passed fully (lint, format, tests) for the first time.
- Merged the PR into `dev` via a merge commit (matching the repository's existing
  convention), keeping the `chore/dev-tooling` branch (not deleted) at the person's request,
  since the branch itself is a low-cost, low-risk thing to keep around for later reference.
- Pulled the merged `dev` locally — fast-forward, all expected files present.

**Engineering decisions:**
- Treated the third CI failure as a design question, not just a bug to patch. Considered
  and rejected making `Settings()` lazy (more invasive, more moving parts, no clear
  additional benefit) in favor of giving CI its own explicit, appropriately-scoped
  configuration — the same pattern every environment (local `.env`, CI's `env:` block,
  eventually a real deployment's environment variables) should independently follow. This
  was initially miscast as a "quick fix" versus "the right fix" tradeoff; on reflection,
  environment-scoped configuration is the standard, correct pattern, not a shortcut.
- Chose "Create a merge commit" over squashing when merging the PR, specifically to
  preserve the individually-readable commit history of the three CI failures and fixes —
  judged more valuable as a record of a real debugging process than a flattened, cleaner-
  looking single commit would have been.
- Kept the merged `chore/dev-tooling` branch rather than deleting it, on request — noted
  that this doesn't affect the repository's real history (all commits are already part of
  `dev` regardless of whether the branch label still exists), so the cost of keeping it is
  purely cosmetic.

**Technical concepts learned:**
- `ruff check` (linting) and `ruff format --check` (formatting) are separate tools/checks
  with separate rule sets — passing one says nothing about the other.
- Why CI runners always start from a fresh checkout of only what's committed to the
  repository — meaning anything `.gitignore`'d (like `.env`) simply does not exist there,
  by design.
- The distinction between a step-scoped `env:` block in a GitHub Actions workflow (applies
  only to one step) versus job-level or workflow-level environment variables.
- Why "the test suite requires real database configuration to even import" was itself a
  design smell, given that `tests/conftest.py` was specifically built to isolate tests from
  any real database.
- The genuine difference between a plausible-looking local test (setting env vars while
  `.env` was still present, which could pass for the wrong reason) and a conclusive one
  (temporarily removing `.env` entirely to eliminate ambiguity


---

## 2026-08-10 — Fixed the broken stored procedures + found the views were out of sync

**Objective:**
Fix the two broken stored procedures, and decide what to do with the two unused views.

**Work completed:**
- Fixed `GetQuestDetails` and `UpdateCharacterStatus` in `sql/procedures.sql` — both
  were missing their `CREATE PROCEDURE` line entirely. Tested all three procedures
  for real in MySQL Workbench, they all work now.
- While checking the views, found something bigger: `sql/views.sql` didn't match
  what's actually in the database at all. The real views in the database are way
  more developed (more joins, more columns) than what's in the file. Pulled the
  real definitions straight from the database and rewrote `sql/views.sql` to
  actually match reality. Added `DROP VIEW IF EXISTS` before each one too, so the
  file can be safely re-run.
- Decided to wire up the two unused views as real endpoints instead of deleting
  them, since they turned out to have genuinely useful data (quest stats, active
  demigod info). Added `/views/quest-statistics` and `/views/active-demigods` to
  `api/main.py`, same pattern as the existing view endpoint. Tested both live —
  both return 200 OK with real data.

**What I learned:**
- A `.sql` file in the repo isn't automatically trustworthy — it can drift from
  what's actually running in the database if someone edits the database directly
  and never updates the file. Worth double-checking instead of assuming.
- `DROP PROCEDURE`/`DROP VIEW ... IF EXISTS` only take a name, never a parameter
  list — that's what was broken in the procedures.
- Leftover environment variables from testing earlier (`DB_USER`/`DB_NAME` set to
  fake CI values) can silently break local testing later in the same terminal
  session — had to clear them before the new endpoints would connect properly.

**Still not done:**
- The live database's `characters` table (and probably `quests`/`monsters` too)
  still has the *old* schema — no real `ENUM` protection yet, since nothing's
  re-run the schema against the new models. This is the actual trigger for
  finally adding Alembic, which was always the plan for "next real schema change."

**Next up:** Alembic (migrations), so the schema drift problem stops happening.