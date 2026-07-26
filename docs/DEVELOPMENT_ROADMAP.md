# MythosAI Development Roadmap

## 1. Project Vision

MythosAI is an AI-powered knowledge and reasoning platform built on a structured model of the Percy Jackson universe.

The project began as a university Database Systems project and is being expanded into a long-term AI engineering project.

The goal is to explore how modern AI systems can combine:

- Relational databases
- Natural-language querying
- Knowledge graphs
- Graph algorithms
- Retrieval-Augmented Generation (RAG)
- Vector search and embeddings
- Agentic AI and tool use
- Open-weight language models
- Machine learning
- AI evaluation
- Fine-tuning
- Production deployment and MLOps

The Percy Jackson universe acts as the initial knowledge domain, but the architecture is intended to demonstrate techniques that could also be applied to enterprise knowledge systems and other large interconnected datasets.

---

# 2. Current System

## Completed

- [x] 13-table normalised relational database
- [x] SQLAlchemy ORM
- [x] FastAPI backend
- [x] REST API
- [x] CRUD operations
- [x] Complex multi-table joins
- [x] Database views
- [x] Stored procedures
- [x] CHECK constraints
- [x] UNIQUE constraints
- [x] Database indexes
- [x] Data population scripts
- [x] Swagger/OpenAPI documentation
- [x] Environment-variable configuration

## Current Technology Stack

### Language
- Python

### Backend
- FastAPI
- SQLAlchemy

### Database
- MariaDB / MySQL
- PyMySQL

### API
- REST
- OpenAPI / Swagger

---

# 3. Target Architecture

The long-term architecture will combine several specialised data and AI systems rather than relying on a single LLM for every task.

```text
                         User
                           |
                           v
                    Frontend Application
                           |
                           v
                        FastAPI
                           |
                           v
                  AI Routing / Agent Layer
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
     SQL Engine       Graph Engine      RAG Engine
          |                |                |
          v                v                v
   Relational DB      Knowledge Graph    Vector DB
          |                |                |
          +----------------+----------------+
                           |
                           v
                    Evidence / Context
                           |
                           v
                      LLM Layer
                    /         \
                   v           v
            Hosted Models   Open Models
                         |
                         v
                 Grounded Response
```

---

# 4. Phase 1 — Core Platform

## Goal

Transform the original university database project into a polished and maintainable full-stack application.

## Tasks

- [ ] Review and clean existing project structure
- [ ] Verify all existing API endpoints
- [ ] Improve error handling
- [ ] Add Pydantic request and response schemas
- [ ] Add automated backend tests
- [ ] Add structured logging
- [ ] Build frontend foundation
- [ ] Create database explorer interface
- [ ] Add search
- [ ] Add filtering
- [ ] Add sorting
- [ ] Add entity detail pages
- [ ] Add basic analytics/dashboard views
- [ ] Improve API documentation
- [ ] Document local development setup

## Technologies

- Python
- FastAPI
- SQLAlchemy
- React or Vue
- pytest
- MariaDB initially
- Potential PostgreSQL migration later

## Completion Criteria

Phase 1 is complete when a user can run MythosAI locally and browse, search and explore the database through a working frontend without directly interacting with SQL or Swagger.

---

# 5. Phase 2 — Natural-Language Database Querying

## Goal

Allow users to query structured database information using natural language.

## Example

User asks:

> Which children of Poseidon have participated in the most quests?

The system should:

1. Receive the natural-language question.
2. Inspect the relevant database schema.
3. Determine which tables and relationships are required.
4. Generate SQL.
5. Validate the generated SQL.
6. Execute the query using read-only database access.
7. Return structured results.
8. Generate a natural-language explanation grounded in those results.

## Tasks

- [ ] Database schema extraction
- [ ] Schema-aware LLM prompting
- [ ] Natural-language-to-SQL generation
- [ ] SQL syntax validation
- [ ] Read-only SQL execution
- [ ] Prevent INSERT, UPDATE, DELETE, DROP and other destructive statements
- [ ] Query row limits
- [ ] Query timeout
- [ ] Results table in frontend
- [ ] Display generated SQL
- [ ] Natural-language explanation
- [ ] Query history
- [ ] Error handling for invalid SQL
- [ ] Retry/correction mechanism

## Evaluation Metrics

Track:

- SQL validity rate
- SQL execution success rate
- Query accuracy
- Final answer accuracy
- Latency
- Token usage
- Cost

---

# 6. Phase 3 — Knowledge Graph

## Goal

Represent relationships between MythosAI entities as a graph and apply graph algorithms to discover information that is difficult to obtain through traditional relational querying alone.

## Potential Nodes

- Characters
- Gods
- Powers
- Quests
- Monsters
- Books
- Locations
- Cabins
- Weapons
- Prophecies

## Potential Relationships

- CHILD_OF
- HAS_POWER
- PARTICIPATED_IN
- FOUGHT
- APPEARS_IN
- USES_WEAPON
- MEMBER_OF
- LOCATED_AT
- CONNECTED_TO
- ASSOCIATED_WITH

## Tasks

- [ ] Convert relational data into graph representation
- [ ] Build graph ingestion pipeline
- [ ] Evaluate NetworkX vs Neo4j
- [ ] Interactive graph visualisation
- [ ] Entity neighbourhood exploration
- [ ] Shortest-path queries
- [ ] Degree centrality
- [ ] Betweenness centrality
- [ ] PageRank
- [ ] Community detection
- [ ] Relationship strength scoring
- [ ] Character network analysis

## Example Questions

- How is Annabeth connected to Tyson?
- Who is the most central character in the universe?
- Which characters act as bridges between different groups?
- Which quests connect otherwise separate character communities?
- What is the shortest relationship path between two characters?

---

# 7. Phase 4 — Retrieval-Augmented Generation (RAG)

## Goal

Allow MythosAI to answer questions requiring unstructured textual knowledge rather than only structured database facts.

## Proposed Pipeline

```text
Documents
    |
    v
Document Processing
    |
    v
Chunking
    |
    v
Embeddings
    |
    v
Vector Database
    |
    v
Semantic Retrieval
    |
    v
Reranking
    |
    v
Context Construction
    |
    v
LLM
    |
    v
Answer + Sources
```

## Tasks

- [ ] Identify appropriate legal/public data sources
- [ ] Document ingestion pipeline
- [ ] Text cleaning
- [ ] Experiment with chunking strategies
- [ ] Embedding generation
- [ ] Vector database
- [ ] Semantic search
- [ ] Metadata filtering
- [ ] Reranking
- [ ] Context construction
- [ ] Source citations
- [ ] Retrieval evaluation
- [ ] Hallucination testing

## Potential Technologies

- pgvector
- Chroma
- FAISS
- Qdrant
- sentence-transformers
- hosted embedding APIs

Technology choices will be evaluated rather than selected purely for resume keywords.

---

# 8. Phase 5 — Hybrid Retrieval and Reasoning

## Goal

Allow MythosAI to determine which knowledge system should answer a question.

Different questions require different retrieval methods.

## Structured Questions

Use SQL.

Example:

> How many quests involved Percy?

## Relationship Questions

Use graph search.

Example:

> How is Percy connected to Athena?

## Semantic Questions

Use RAG.

Example:

> Explain how Percy's relationship with Poseidon develops.

## Hybrid Questions

Use multiple systems.

Example:

> Which characters have similar quest histories to Percy and also have similar relationships with their godly parents?

This may require:

1. SQL retrieval
2. Graph analysis
3. Semantic retrieval
4. Evidence aggregation
5. LLM synthesis

## Tasks

- [ ] Query classifier
- [ ] SQL router
- [ ] Graph router
- [ ] Vector retrieval router
- [ ] Hybrid routing
- [ ] Evidence aggregation
- [ ] Context management
- [ ] Confidence scoring
- [ ] Fallback strategies
- [ ] Routing evaluation

---

# 9. Phase 6 — Agentic AI

## Goal

Allow an AI model to solve multi-step questions by selecting and using specialised MythosAI tools.

## Potential Tools

```text
search_character()
get_character()
get_character_relationships()
query_database()
find_shortest_path()
calculate_centrality()
search_documents()
compare_characters()
calculate_similarity()
get_quest_history()
get_monster_encounters()
```

## Example

User asks:

> Compare Percy and Jason based on powers, quest experience and relationships.

The agent may:

1. Retrieve Percy.
2. Retrieve Jason.
3. Query powers.
4. Query quest participation.
5. Analyse graph relationships.
6. Calculate similarity.
7. Retrieve relevant semantic context.
8. Combine the evidence.
9. Generate the final comparison.

## Tasks

- [ ] Define AI tools
- [ ] Tool-calling interface
- [ ] Agent state
- [ ] Multi-step workflows
- [ ] Planning
- [ ] Tool result validation
- [ ] Error recovery
- [ ] Maximum step limits
- [ ] Tool usage logs
- [ ] Agent evaluation

---

# 10. Phase 7 — Open-Weight Language Models

## Goal

Experiment with running and evaluating open-weight models rather than relying exclusively on hosted AI APIs.

## Candidate Model Families

- Llama
- Qwen
- DeepSeek
- Mistral

Specific models will be selected based on available hardware, licensing, model capabilities and project requirements.

## Potential Technologies

- Ollama
- vLLM
- Hugging Face Transformers

## Experiments

- [ ] Local inference
- [ ] Hosted open-model inference
- [ ] CPU inference
- [ ] GPU inference
- [ ] FP16 inference
- [ ] INT8 quantisation
- [ ] 4-bit quantisation
- [ ] Model routing
- [ ] Structured output performance
- [ ] Tool-calling performance
- [ ] Text-to-SQL performance
- [ ] Cost comparison
- [ ] Latency comparison
- [ ] Accuracy comparison

## Benchmarking

Track results such as:

| Model | Answer Accuracy | SQL Validity | Latency | Memory | Cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| Model A | TBD | TBD | TBD | TBD | TBD |
| Model B | TBD | TBD | TBD | TBD | TBD |
| Model C | TBD | TBD | TBD | TBD | TBD |

The goal is to understand the trade-offs between model quality, speed, memory requirements, privacy and cost.

---

# 11. Phase 8 — Machine Learning and Recommendation Systems

## Goal

Add statistical and machine-learning capabilities beyond LLM-based functionality.

## Character Similarity Engine

Potential features:

- Godly parent
- Powers
- Power levels
- Quest participation
- Quest difficulty
- Monster encounters
- Weapon types
- Locations
- Affiliations
- Relationships

## Experiments

- [ ] Feature engineering
- [ ] Feature normalisation
- [ ] One-hot encoding
- [ ] Cosine similarity
- [ ] k-nearest neighbours
- [ ] Clustering
- [ ] Dimensionality reduction
- [ ] Embedding-based similarity
- [ ] Compare classical feature vectors with embeddings

## Example Output

```text
Characters Most Similar to Percy Jackson

1. Character A — 87%
2. Character B — 79%
3. Character C — 72%
```

The system should also explain which features contributed to the similarity score.

---

# 12. Phase 9 — AI Evaluation Framework

## Goal

Build a repeatable benchmark for evaluating MythosAI rather than judging AI quality manually.

## Benchmark Categories

- Simple SQL questions
- Aggregation questions
- Complex SQL
- Multi-table joins
- Graph reasoning
- Semantic retrieval
- Hybrid reasoning
- Multi-step agent tasks
- Ambiguous questions
- Adversarial prompts

## Metrics

Potential metrics include:

- Answer correctness
- SQL correctness
- SQL execution success
- Retrieval precision
- Retrieval recall
- Context relevance
- Hallucination rate
- Tool selection accuracy
- Routing accuracy
- Latency
- Token usage
- Cost

## Tasks

- [ ] Create benchmark question dataset
- [ ] Define expected answers
- [ ] Define expected SQL where appropriate
- [ ] Automated evaluation runner
- [ ] Model comparison reports
- [ ] Regression testing
- [ ] Track performance between releases
- [ ] Visualise benchmark results

---

# 13. Phase 10 — Security and AI Guardrails

## Goal

Make interaction between AI models, users and the database safe.

## Database Security

- [ ] Dedicated read-only AI database role
- [ ] SELECT-only permissions
- [ ] SQL allowlist
- [ ] SQL parser validation
- [ ] Query timeout
- [ ] Result limits

## AI Security

- [ ] Prompt injection testing
- [ ] Jailbreak testing
- [ ] Input validation
- [ ] Output validation
- [ ] Tool permission controls
- [ ] Agent step limits

## Application Security

- [ ] Rate limiting
- [ ] Secret management
- [ ] Authentication
- [ ] Authorisation
- [ ] Dependency vulnerability scanning
- [ ] Security logging

---

# 14. Phase 11 — Production Engineering

## Goal

Deploy MythosAI as a production-style AI application rather than only a local development project.

## Containerisation

- [ ] Dockerise backend
- [ ] Dockerise frontend
- [ ] Docker Compose
- [ ] Database container for development
- [ ] Redis container
- [ ] Local model container where appropriate

## CI/CD

- [ ] GitHub Actions
- [ ] Automated tests
- [ ] Linting
- [ ] Build validation
- [ ] Security checks
- [ ] Automated deployment

## Cloud

- [ ] Select cloud platform
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Managed relational database
- [ ] Object storage
- [ ] HTTPS
- [ ] Environment/secrets management
- [ ] Domain configuration

## Performance

- [ ] Redis caching
- [ ] Query caching
- [ ] Embedding caching
- [ ] LLM response caching where appropriate
- [ ] Database connection pooling
- [ ] Performance testing

---

# 15. Phase 12 — Observability

## Goal

Understand what the AI system is doing and identify failures, bottlenecks and expensive operations.

## Track

- User question
- Selected retrieval route
- Selected model
- Tool calls
- Generated SQL
- SQL execution time
- Retrieved documents
- Retrieval scores
- LLM latency
- Total request latency
- Token usage
- Estimated cost
- Errors
- Final response status

## Potential Technologies

- OpenTelemetry
- Prometheus
- Grafana
- LangSmith
- Custom application dashboards

## Tasks

- [ ] Structured application logging
- [ ] Request tracing
- [ ] AI trace logging
- [ ] Performance metrics
- [ ] Error monitoring
- [ ] Cost monitoring
- [ ] Model usage dashboard
- [ ] Retrieval performance dashboard

---

# 16. Phase 13 — Fine-Tuning and Small Language Model Research

## Goal

Investigate whether adapting smaller models to narrow MythosAI tasks can outperform or reduce the cost of general-purpose models.

## Potential Experiment

Fine-tune a small model specifically for:

Natural language -> MythosAI SQL

## Dataset

Create examples containing:

```text
Natural-language question
        |
        v
Expected SQL query
```

## Experiments

- [ ] Build question-to-SQL dataset
- [ ] Establish zero-shot baseline
- [ ] Establish few-shot baseline
- [ ] Prompt engineering experiments
- [ ] LoRA fine-tuning
- [ ] QLoRA fine-tuning
- [ ] Compare base vs prompted vs fine-tuned model
- [ ] Evaluate accuracy
- [ ] Evaluate latency
- [ ] Evaluate memory requirements
- [ ] Evaluate inference cost

The objective is not simply to fine-tune a model, but to measure whether fine-tuning provides a meaningful improvement.

---

# 17. Phase 14 — Model Context Protocol (MCP)

## Goal

Explore exposing MythosAI capabilities as tools that compatible external AI systems can use.

## Potential MCP Tools

- Character search
- Character details
- Database querying
- Quest lookup
- Graph exploration
- Relationship path finding
- Semantic retrieval
- Character similarity calculation

## Potential Architecture

```text
External AI Client
        |
        v
       MCP
        |
        v
MythosAI Tool Server
        |
   +----+----+
   |    |    |
  SQL  Graph RAG
```

## Tasks

- [ ] Research current MCP specification
- [ ] Define safe MythosAI tools
- [ ] Implement MCP server
- [ ] Add authentication where appropriate
- [ ] Test external AI client integration
- [ ] Evaluate security implications

---

# 18. Potential Future Research

These features are intentionally lower priority and should only be explored after the core architecture is working.

## Possible Extensions

- [ ] Multimodal search
- [ ] Image-based retrieval
- [ ] Timeline reasoning
- [ ] Temporal knowledge graphs
- [ ] Automatic knowledge graph extraction
- [ ] Ensemble model routing
- [ ] Dynamic model selection
- [ ] Model confidence calibration
- [ ] Synthetic training data
- [ ] Recommendation systems
- [ ] User-personalised retrieval
- [ ] Streaming AI responses
- [ ] WebSockets
- [ ] Distributed inference
- [ ] Advanced caching strategies
- [ ] Automated data ingestion
- [ ] Human feedback collection
- [ ] A/B testing of AI models

---

# 19. Development Workflow

MythosAI uses a structured Git workflow.

```text
feature branch
      |
      v
     dev
      |
      v
     main
```

## Main Branch

`main` represents the stable version of MythosAI.

Features should only reach `main` once they are tested and considered stable.

## Development Branch

`dev` is the primary integration branch and the default GitHub branch.

Completed features are merged into `dev` through pull requests.

## Feature Branches

Individual features should be developed on dedicated branches.

Examples:

```text
feature/frontend-foundation
feature/database-explorer
feature/text-to-sql
feature/sql-guardrails
feature/knowledge-graph
feature/rag-pipeline
feature/hybrid-router
feature/agent-tools
feature/open-weight-models
feature/model-evaluation
```

---

# 20. Development Principles

1. Build one working layer at a time.
2. Keep `main` stable.
3. Use feature branches for new functionality.
4. Merge features into `dev` through pull requests.
5. Do not add technology purely for resume keywords.
6. Every major feature should solve a defined problem.
7. AI-generated answers should be grounded in project data whenever possible.
8. Evaluate AI functionality rather than relying only on subjective testing.
9. Prefer measurable improvements over unsupported claims.
10. Keep planned and implemented functionality clearly separated.
11. Document important architectural decisions.
12. Build security into AI/database interactions from the beginning.
13. Prefer simple architectures until additional complexity is justified.
14. Treat failures and unsuccessful experiments as useful engineering results.
15. Continuously improve documentation as the system evolves.

---

# 21. Immediate Development Priorities

The long-term roadmap is intentionally ambitious. Development should occur incrementally.

## Current Priority

### Milestone 1 — Portfolio-Ready Core

- [ ] Clean existing backend
- [ ] Verify database functionality
- [ ] Verify existing API endpoints
- [ ] Add automated tests
- [ ] Build frontend foundation
- [ ] Build database explorer
- [ ] Add search and filtering

### Milestone 2 — First AI Capability

- [ ] Add natural-language-to-SQL
- [ ] Add SQL safety validation
- [ ] Execute read-only AI-generated queries
- [ ] Display query results
- [ ] Generate database-grounded explanations

### Milestone 3 — Deploy

- [ ] Dockerise application
- [ ] Add CI/CD
- [ ] Deploy frontend
- [ ] Deploy backend
- [ ] Deploy database
- [ ] Add basic monitoring

Once these milestones are complete, MythosAI will already function as a substantial AI engineering portfolio project.

The later phases can then be implemented gradually as the project and my AI/ML knowledge develop.

---

# 22. Project Status

MythosAI is under active development.

Completed checklist items represent functionality that has been implemented and verified.

Unchecked items represent planned features, experiments or research directions and should not be interpreted as currently implemented functionality.

This roadmap is expected to evolve as the architecture develops and new technical decisions are made.