# MythosAI architecture

This document describes the finished local MVP. The [README](../README.md) is the project overview; earlier roadmap documents preserve historical planning.

## Components

| Component | Responsibility |
|---|---|
| `frontend/` | Single Ask experience in vanilla HTML, CSS, and JavaScript |
| `api/main.py` | FastAPI application, UI at `/`, static assets at `/assets`, API routers |
| `api/answers.py` | `POST /ask` orchestration and application-owned response assembly |
| `answer_context.py` | Deterministic selection of relational character/god facts |
| `retrieval.py`, `corpus/sources.json` | Local TF-IDF/cosine retrieval and attributed summary metadata |
| `llm.py` | One HTTP boundary to local LM Studio; model response parsing |
| `schemas/answer.py` | Pydantic request, generated-output, fact, and response contracts |
| `models/` | SQLAlchemy relational models, settings, and database sessions |
| `scripts/evaluate.py`, `evaluation/` | Fixed offline context-selection evaluation |

## Ask request lifecycle

1. The frontend posts a question to the same-origin `/ask` endpoint. Pydantic trims it, requires at least one letter, limits it to 2,000 characters, and rejects extra request fields.
2. The application retrieves up to three positive-scoring corpus passages and selects database facts.
3. If both collections are empty, it returns the standard insufficient-context answer without invoking LM Studio.
4. Otherwise, `generate_answer()` sends the question, facts, and evidence as JSON context alongside grounding instructions.
5. The application parses the returned JSON into `GeneratedAnswer`. The model may provide only a nonblank `answer` string and an `insufficient_context` boolean.
6. The application assembles `AskResponse`: `question`, `answer`, `insufficient_context`, `facts`, and `evidence`. If the model reports insufficient context, the API substitutes the standard insufficient-context message.
7. The frontend renders answer text, grouped database facts, and source-linked evidence separately. Text is inserted as text content, not rendered as model-generated HTML.

Facts and evidence come from application code, never from model-generated citations or profiles. Pydantic validates structure; it does not verify factual truth or independently check whether every answer claim follows from the context.

## Relational context

The normal application connects to **MySQL/MariaDB through PyMySQL**. The schema has ten core entity tables and three junction tables. The Ask pipeline uses only selected god/character profiles and their parent/power relationships, rather than querying every part of that schema.

Name matching is case-insensitive and respects word boundaries. It recognizes full names, gods' Roman names, and unambiguous character first names. At most three matched profiles are included, with at most five powers per character. This is deterministic profile selection, not natural-language-to-SQL.

Database facts are project data. A source attached to an evidence summary does not certify the database fields.

SQLAlchemy's `get_db()` dependency closes each request session. Existing entity, join, view, and stored-procedure endpoints remain available alongside Ask. Alembic tracks schema changes; fresh setup requires table creation and the separate view/procedure scripts described in [local setup](LOCAL_SETUP.md).

## Evidence retrieval and provenance

The corpus contains **12 short project-authored factual summaries from six official Rick Riordan pages**. Each record carries a stable source ID, title, reference, source URL, `attributed_summary` provenance, text, and tags. See [corpus coverage](../corpus/README.md).

Retrieval tokenizes titles, text, and tags, normalizes case, excludes a small stop-word set, and ranks TF-IDF vectors by cosine similarity. Only positive matches are returned; ties use source ID. The corpus is loaded and scored on each call. No embeddings, vector database, synonym expansion, or external search is involved.

Scores represent lexical similarity, not confidence. They are present in the API response but are not displayed as confidence percentages. Source links must be HTTP(S) URLs without credentials. Evidence passages are paraphrases, not direct quotations, and attribution is limited to each summary.

## Local generation and errors

Settings in `models/config.py` read environment variables or `.env`:

| Setting | Default |
|---|---|
| `LM_STUDIO_BASE_URL` | `http://127.0.0.1:1234` |
| `LM_STUDIO_MODEL` | `qwen/qwen3-4b-2507` |
| `LM_STUDIO_TIMEOUT_SECONDS` | `120` |

The single inference path uses `httpx.post()` to `/v1/chat/completions`. Requests use system/user messages, `stream: false`, `max_tokens: 800`, and `response_format.type: json_schema` with the generated-output Pydantic schema. No API key is sent.

The parser requires one choice with `finish_reason: stop`, rejects tool calls/refusals, validates the message content as JSON, and rejects blank answers. Grounding instructions limit generation to supplied context, but compliance is not a factual guarantee.

| Condition | HTTP response |
|---|---|
| LM Studio connection failure | 503, local server unavailable |
| Inference timeout | 504, local server timed out |
| Other provider HTTP failures | 502, request failed |
| Malformed, incomplete, or invalid model output | 502, invalid response |

Public errors omit provider response bodies. There is no fallback provider, retry workflow, or fabricated success response. The configured timeout is passed to httpx; it is not a measured model-performance target.

## Tests, evaluation, and boundaries

Backend tests replace the application database with isolated in-memory SQLite and mock inference. Frontend tests use Node's test runner. GitHub Actions runs both suites and Ruff on pushes/PRs targeting `dev` and `main`; it does not run a live model.

The [offline evaluation](../evaluation/results.json) uses an independent SQLite fixture containing two gods, two characters, and two powers. Its 18 cases measure retrieval, selected entities/facts, and the empty-context gate. Seventeen pass all applicable checks; Case 08 exposes a lexical paraphrase miss. Unsupported questions with related context still need model judgment, which is explicitly not evaluated.

This is a local MVP with one Ask experience. It has no agent workflow, generated SQL, graph retrieval, authentication layer, or deployment pipeline. Future ideas in historical roadmaps are not part of this architecture.
