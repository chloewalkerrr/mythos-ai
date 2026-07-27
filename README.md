# MythosAI

> An AI-powered knowledge and reasoning platform built on a structured model of the Percy Jackson universe.

**Status:** 🚧 Active Development

MythosAI is an ongoing AI engineering and data systems project exploring how large language models, relational databases, knowledge graphs, retrieval systems, and machine learning can work together to answer complex questions over structured and unstructured knowledge.

The project began as a university Database Systems project focused on relational database design. I am now independently extending it into a larger AI knowledge and reasoning platform.

---

## Current System

The current implementation provides the relational data, API, testing, and backend engineering foundation for MythosAI.

### Current Features

- 13-table normalised relational database
- SQLAlchemy ORM models
- FastAPI REST API
- CRUD operations
- Complex multi-table joins
- Database views
- Stored procedures
- Database indexing
- CHECK and UNIQUE constraints
- Sample data population scripts
- Interactive FastAPI / OpenAPI documentation
- Pydantic request validation
- Pydantic response models
- Modular FastAPI routers
- Environment-based database configuration
- Parameterised stored procedure queries

The database models relationships between:

- Characters
- Gods
- Cabins
- Powers
- Weapons
- Quests
- Monsters
- Locations
- Books
- Prophecies

---

## Current Tech Stack

### Language

- Python

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### Database

- MariaDB / MySQL
- PyMySQL
- SQLite for automated testing

### Testing and Code Quality

- pytest
- Ruff

### Development

- Git
- GitHub
- GitHub Actions
- VS Code

---

# Engineering Foundation

Since the original university database project, MythosAI has been extended with a stronger software engineering foundation.

Current engineering improvements include:

- FastAPI route separation using `APIRouter`
- Pydantic request and response validation
- JSON-based character create and update operations
- Automated API testing with pytest
- An isolated SQLite database for automated tests
- 17 backend tests covering CRUD, relationships, joins, validation, and error handling
- Ruff linting and formatting
- GitHub Actions continuous integration
- Feature-branch and pull-request workflow
- Environment-variable based configuration
- Parameterised SQL for user-provided stored procedure input

These improvements were introduced incrementally while using automated tests to preserve existing behaviour.

---

# Testing and Continuous Integration

MythosAI uses pytest for automated backend testing.

The current test suite covers:

- API documentation availability
- OpenAPI schema generation
- Character retrieval
- Character creation
- Character updates
- Character deletion
- Input validation
- Missing-resource responses
- God-to-character relationships
- Character powers
- Character quest participation
- Relational join endpoints

Tests use an isolated SQLite database rather than the local MariaDB development database.

This keeps automated tests repeatable and prevents the test suite from modifying local development data.

Run the test suite with:

```bash
python -m pytest
```

Ruff is used for Python linting and formatting:

```bash
python -m ruff check .
python -m ruff format . --check
```

GitHub Actions automatically runs the quality checks and test suite on pull requests into `dev` and `main`.

---

# Current Backend Architecture

The backend currently uses a lightweight modular FastAPI structure.

```text
mythos-ai/
├── api/
│   ├── main.py
│   ├── characters.py
│   ├── gods.py
│   └── quests.py
│
├── models/
│   ├── base.py
│   ├── character.py
│   ├── god.py
│   └── all_models.py
│
├── schemas/
│   ├── __init__.py
│   └── character.py
│
├── scripts/
│   ├── create_tables.py
│   └── populate_data.py
│
├── sql/
│   ├── procedures.sql
│   └── views.sql
│
├── tests/
│   ├── conftest.py
│   └── test_api.py
│
├── docs/
│   └── DEVELOPMENT_ROADMAP.md
│
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

The architecture is intentionally being kept lightweight while the project is still growing. New abstractions are introduced only when they solve a clear maintainability or scalability problem.

---

# Project Vision

The long-term goal of MythosAI is to investigate how different AI and data architectures can work together to reason over a connected knowledge domain.

Rather than relying solely on an LLM's internal knowledge, MythosAI will retrieve information from its own structured and unstructured data sources before generating answers.

The planned architecture combines:

- Relational data querying
- Natural-language-to-SQL
- Knowledge graphs
- Graph algorithms
- Retrieval-Augmented Generation (RAG)
- Vector search and embeddings
- Agentic tool use
- Open-weight language models
- Machine learning
- Model evaluation and benchmarking

---

# Development Roadmap

A more detailed technical roadmap is available in:

`docs/DEVELOPMENT_ROADMAP.md`

## Phase 1 — Core Platform

- [x] Relational database design
- [x] SQLAlchemy ORM
- [x] FastAPI backend
- [x] CRUD operations
- [x] Complex joins
- [x] Database views
- [x] Stored procedures
- [x] Database constraints and indexes
- [x] Automated API testing
- [x] Ruff linting and formatting
- [x] GitHub Actions CI
- [x] Pydantic request validation
- [x] Pydantic response models
- [x] Modular API routers
- [x] SQL parameterisation for stored procedure input
- [ ] Frontend application
- [ ] Dockerised development environment

## Phase 2 — Natural-Language Database Querying

- [ ] Natural-language-to-SQL pipeline
- [ ] Schema-aware LLM prompting
- [ ] SQL validation and safety guardrails
- [ ] Read-only AI database access
- [ ] Database-grounded natural-language responses
- [ ] Query history and explanations

Example:

> "Which children of Poseidon have participated in the most quests?"

MythosAI will translate the question into a database query, execute it against the project's data, and generate an explanation grounded in the returned results.

## Phase 3 — Knowledge Graph

- [ ] Transform relational relationships into a graph representation
- [ ] Interactive knowledge graph visualisation
- [ ] Shortest-path relationship queries
- [ ] Degree and betweenness centrality
- [ ] PageRank experiments
- [ ] Community detection
- [ ] Character relationship analysis

## Phase 4 — Retrieval-Augmented Generation

- [ ] Unstructured document ingestion
- [ ] Text chunking pipeline
- [ ] Embedding generation
- [ ] Vector database
- [ ] Semantic search
- [ ] Reranking
- [ ] Source-grounded responses with citations
- [ ] Hybrid structured + unstructured retrieval

## Phase 5 — Hybrid AI Reasoning

Develop a routing layer capable of selecting the appropriate knowledge system for each question:

```text
User Question
      |
      v
  AI Router
      |
  +---+---+
  |   |   |
 SQL Graph RAG
  |   |   |
  +---+---+
      |
      v
Grounded Answer
```

- [ ] Question classification
- [ ] SQL retrieval
- [ ] Graph retrieval
- [ ] Vector retrieval
- [ ] Hybrid retrieval
- [ ] Evidence aggregation

## Phase 6 — Agentic AI

- [ ] LLM tool calling
- [ ] Multi-step task execution
- [ ] Database query tools
- [ ] Graph analysis tools
- [ ] Retrieval tools
- [ ] Agent state and reasoning workflows

## Phase 7 — Open-Weight Models

Experiment with running AI models independently rather than relying exclusively on hosted APIs.

Planned experiments include:

- [ ] Local model inference
- [ ] Llama
- [ ] Qwen
- [ ] DeepSeek
- [ ] Model quantisation
- [ ] Hosted vs local model comparison

Models will be evaluated on factors such as:

- Query accuracy
- SQL generation accuracy
- Response quality
- Latency
- Memory requirements
- Cost

## Phase 8 — Machine Learning and Recommendations

- [ ] Character feature engineering
- [ ] Character similarity scoring
- [ ] Cosine similarity
- [ ] Clustering experiments
- [ ] Recommendation system
- [ ] Compare traditional ML methods with embedding-based similarity

## Phase 9 — AI Evaluation

Build a benchmark dataset for systematically evaluating the AI system.

Planned evaluation categories:

- Simple SQL questions
- Complex joins
- Graph reasoning
- Semantic retrieval
- Hybrid reasoning
- Adversarial queries

Potential metrics include:

- Answer accuracy
- SQL execution success
- Retrieval accuracy
- Hallucination rate
- Latency
- Token usage
- Cost

## Phase 10 — Production Engineering

- [ ] Docker
- [x] CI
- [ ] CD
- [ ] Cloud deployment
- [ ] Redis caching
- [ ] Authentication
- [ ] Rate limiting
- [ ] Logging
- [ ] Observability
- [ ] Performance monitoring

## Future Research

Potential longer-term experiments include:

- Fine-tuning a small language model for schema-specific text-to-SQL
- LoRA / QLoRA fine-tuning
- Model Context Protocol (MCP)
- Small Language Models (SLMs)
- Multimodal retrieval
- Advanced model routing
- Automated model evaluation

---

# Development Workflow

Development primarily occurs from the `dev` branch.

New work is completed on focused branches such as:

```text
feature/...
refactor/...
test/...
fix/...
docs/...
```

Changes are tested locally and merged through pull requests.

`main` is intended to represent the stable version of the project, while `dev` is used as the primary integration branch.

---

# Security

Database credentials and API keys are stored using environment variables rather than being committed to the repository.

The repository includes `.env.example` to document expected configuration while the real `.env` file is excluded through `.gitignore`.

Database calls involving user-provided stored procedure parameters use parameterised SQL rather than direct string interpolation.

Future AI-generated SQL functionality will use additional safeguards such as read-only database access, query validation, execution limits, and restricted SQL operations.

---

# Why Percy Jackson?

The Percy Jackson universe provides a useful test domain because it contains a large number of interconnected entities and relationships — characters, gods, powers, quests, monsters, locations, books, and prophecies.

This makes it suitable for experimenting with:

- Relational querying
- Graph algorithms
- Semantic retrieval
- Recommendation systems
- Natural-language database interaction
- AI reasoning

while keeping the domain understandable and visually interesting.

---

# Project Background

The original database was developed as a university Database Systems project.

The initial project focused on:

- Relational modelling
- Normalisation
- SQL
- ORM integration
- Constraints
- Indexing
- Views
- Stored procedures
- Basic API development

Rather than leaving the project as completed coursework, I decided to continue developing it independently into a broader project focused on databases, data systems, machine learning, and artificial intelligence.

---

# AI Assistance

AI tools have been used during the continued development of MythosAI to discuss architecture, scalability, testing strategies, debugging approaches, documentation, and implementation options.

I review, test, and understand changes before including them in the project. The project is also being used as a way to strengthen my own understanding of backend engineering, database systems, AI engineering, and production software development.

---

# Development Status

MythosAI is under active development.

The backend engineering foundation is now largely complete, and development is moving toward user-facing data exploration and AI functionality.

Completed roadmap items represent implemented and tested functionality. Unchecked items represent planned features, experiments, or research directions rather than functionality that is currently available.