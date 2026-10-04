# Verified local setup

Verified on 2026-10-01 with Python 3.13.3, the existing `venv`, and XAMPP
MariaDB 10.4.32 on Windows. A fresh database was created and populated using
the commands below; dependency installation into a fresh virtual environment
was not tested. No setup code or migration changes were required.

## Prerequisites

- Run commands from the repository root in PowerShell.
- Have Python 3.13 and an environment containing the dependencies in
  `requirements.txt`. Commands below use the existing `venv`.
- Start the existing XAMPP MySQL/MariaDB server on port 3306. On the verified
  machine, the separate `MySQL80` service listens on 3307 and does not serve
  the configured project database.
- Configure `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, and `DB_NAME`
  through `.env` or environment variables. `.env.example` lists the keys.
  Environment variables override `.env`; remove any dummy values left over
  from running tests. No LLM keys are needed.
- For fresh setup, the database account needs permission to create the
  database, tables, views, and procedures and insert sample data.

Enable UTF-8 in the PowerShell session before running Python setup commands.
The scripts print checkmarks that fail under Windows cp1252 output encoding:

```powershell
$env:PYTHONUTF8 = '1'
```

## Existing project database: shortest path

The existing configured database was inspected and already contains the sample
data, current enum columns, all three stored procedures, the API's three
views, and Alembic revision `c002697e0070`. It needs no initialization,
reseeding, or migration for this change.

With XAMPP MariaDB running and the existing `.env` available:

```powershell
.\venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/` for the Ask UI or
`http://127.0.0.1:8000/docs` for the API documentation. Ask requests with
matching context also require the LM Studio setup below. Stop the API with Ctrl+C.
`API_HOST` and `API_PORT` in `.env` are not consumed by the application;
the Uvicorn arguments above select its address.

## Fresh database: verified initialization sequence

Use a new, empty database. Do not run this initialization sequence against
the existing populated project database. The sample-data script inserts
records unconditionally and commits in batches; it must not be rerun after
successful population. A failed partial population also requires inspection
before retrying.

The example below uses `mythosai_local` and the local `root` account.
Substitute your configured host, port, and user in the MySQL commands.
`--password` prompts for the password; press Enter if it is empty.

```powershell
& C:\xampp\mysql\bin\mysql.exe --host=localhost --port=3306 --user=root --password --execute="CREATE DATABASE mythosai_local CHARACTER SET utf8mb4;"
$env:DB_NAME = 'mythosai_local'

.\venv\Scripts\python.exe -m scripts.create_tables
.\venv\Scripts\python.exe -m alembic stamp head
.\venv\Scripts\python.exe -m scripts.populate_data

& C:\xampp\mysql\bin\mysql.exe --host=localhost --port=3306 --user=root --password --default-character-set=utf8mb4 mythosai_local --execute="source sql/views.sql"
& C:\xampp\mysql\bin\mysql.exe --host=localhost --port=3306 --user=root --password --default-character-set=utf8mb4 mythosai_local --execute="source sql/procedures.sql"

.\venv\Scripts\python.exe -m alembic check
.\venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Run each command only after the preceding one succeeds. The `DB_NAME`
override applies only to this PowerShell session; set it in `.env` if this
new database should be used in later sessions.

`create_tables` creates the current model schema. `stamp head` records that
schema's migration revision without running an alteration. This stamping
step applies only to the freshly created current schema, not an arbitrary
existing database. The only migration alters existing columns, so
`alembic upgrade head` alone cannot initialize an empty database.

Views and procedures require the separate SQL commands. Neither table
creation nor Alembic installs them. The historical `backup.sql` is not
needed for this path.

## Database verification results (2026-10-01)

- Fresh database: 13 domain tables, 61 sample rows, 7 characters, and the
  recorded Alembic revision `c002697e0070`.
- `alembic check`: no new upgrade operations detected.
- 20 HTTP checks passed on each of the existing and fresh databases:
  documentation/OpenAPI, all 10 entity lists, character detail, both
  character joins, god children, all three view endpoints, and the
  god-children stored-procedure endpoint.
- On fresh MariaDB, an invalid character-status update returned 422;
  the stored value remained `alive` and the character remained readable.

Verification used temporary database names and available local HTTP ports.
The temporary databases were removed and the verification API processes
stopped. The existing project database received read requests only.

## Python environment for a new checkout

The database verification above used an existing environment. For a new
checkout, create one and install the pinned dependencies from the repository root:

```powershell
py -3.13 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Copy the example only when creating a new `.env`; preserve any existing local
configuration. Set the database variables in that file before importing the
application or running database scripts. A fresh dependency installation was
not part of the recorded database verification.

The UI needs no frontend build or npm installation. Node 22 is used by CI for
the frontend tests, not for serving the application.

## LM Studio and the Ask UI

The local setup uses **LM Studio 0.4.25** with **Qwen3 4B Instruct 2507,
Q4_K_M**, served under the model identifier `qwen/qwen3-4b-2507`.

1. Load that model in LM Studio.
2. Start LM Studio's local server at `http://127.0.0.1:1234`.
3. Keep MySQL/MariaDB running and use the configured, populated project database.
4. Confirm these values in `.env` (they match the application defaults):

```dotenv
LM_STUDIO_BASE_URL=http://127.0.0.1:1234
LM_STUDIO_MODEL=qwen/qwen3-4b-2507
LM_STUDIO_TIMEOUT_SECONDS=120
```

The base URL is the server root: the application appends
`/v1/chat/completions`. No API key is required. The application uses chat
completions with JSON-schema response formatting and validates the returned
JSON structure itself with Pydantic; it does not use the OpenAI Responses API.

Start the production application:

```powershell
.\venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Visit `http://127.0.0.1:8000/` and ask **“Who is Percy Jackson's parent?”**.
A successful result shows the answer, database facts, and attributed evidence
with source links. The development-only `scripts.preview_frontend` server
uses mocks and is not an end-to-end inference check.

Local inference can take roughly a minute or longer on the tested Snapdragon X
machine. The 120-second setting is passed to httpx for provider timeouts; it is
not a response-time guarantee. An unavailable LM Studio server produces 503,
a provider timeout produces 504, and invalid model output or other provider
HTTP failures produce 502. The application does not switch providers or invent
an answer when a request fails.

## Offline tests and evaluation

Run with the project virtual environment active, or substitute its full Python path:

```powershell
python -m pytest
node --test tests/frontend/app.test.mjs
python -m ruff check .
python -m ruff format --check .
python -m scripts.evaluate
```

Tests and evaluation use isolated SQLite fixtures and no live model calls.
They still import settings: retain `DB_USER` and `DB_NAME` in `.env`, or set
dummy values in a separate test shell. No running MariaDB server is required.

The evaluator prints the full report without changing the saved results.
It currently exits **1** for the known Case 08 paraphrase failure (17/18 cases
pass). That is a recorded retrieval limitation, not a model-accuracy score or
a failure of the automated test suite. See [the saved results](../evaluation/results.json).
