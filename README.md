# MythosAI

> An AI-powered knowledge and reasoning platform built on a structured model of the Percy Jackson universe.

**Status:** 🚧 Active Development

MythosAI is an ongoing AI engineering and data systems project exploring how large language models, relational databases, knowledge graphs, retrieval systems, and machine learning can work together to answer complex questions over structured and unstructured knowledge.

The project began as a Database Systems university project focused on relational database design. I am now independently extending it into a larger AI knowledge and reasoning platform.

---

## Current System

The current implementation provides the data and backend foundation for MythosAI.

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
- Interactive FastAPI API documentation

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

**Language**
- Python

**Backend**
- FastAPI
- SQLAlchemy

**Database**
- MariaDB / MySQL
- PyMySQL

**API**
- REST
- OpenAPI / Swagger

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

## Phase 1 — Core Platform

- [x] Relational database design
- [x] SQLAlchemy ORM
- [x] FastAPI backend
- [x] CRUD operations
- [x] Complex joins
- [x] Database views
- [x] Stored procedures
- [x] Database constraints and indexes
- [ ] Frontend application
- [ ] Expanded automated testing
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

## Phase 8 — Machine Learning & Recommendations

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
- [ ] CI/CD
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

# Why Percy Jackson?

The Percy Jackson universe provides a useful test domain because it contains a large number of interconnected entities and relationships — characters, gods, powers, quests, monsters, locations, books, and prophecies.

This makes it suitable for experimenting with relational querying, graph algorithms, semantic retrieval, recommendations, and AI reasoning while keeping the domain understandable and visually interesting.

---

# Project Background

The original database was developed as a university Database Systems project. The initial project focused on relational modelling, normalisation, SQL, ORM integration, constraints, indexing, views, stored procedures, and API development.

MythosAI represents the continued independent development of that foundation into a broader AI engineering project.

---

## Development Status

MythosAI is under active development.

Completed roadmap items represent implemented functionality. Unchecked items represent planned features and experiments rather than functionality currently available.