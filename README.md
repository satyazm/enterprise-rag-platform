# Enterprise RAG Platform

An internal enterprise AI knowledge platform — not another PDF chatbot. Built to demonstrate production-grade RAG patterns: multi-document ingestion, hybrid search, citation-based answers, conversation memory, role-based access, evaluation pipelines, observability, and agentic workflows.

## Architecture

```
                        ┌───────────────┐
                        │   Frontend    │
                        │ Next.js/React │
                        └───────┬───────┘
                                │
                                ▼
                      ┌──────────────────┐
                      │ FastAPI Backend  │
                      └───────┬──────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
         Auth Service    Chat Service   Ingestion Service
                              │
                              ▼
                    LangGraph Workflow
                              │
     ┌────────────────────────┼────────────────────────┐
     ▼                        ▼                        ▼
Query Understanding    Retrieval Agent        Answer Agent
                              │
                              ▼
                      Hybrid Retrieval
                ┌─────────────┼─────────────┐
                ▼                           ▼
         Vector Search              BM25 Search
                ▼                           ▼
          Qdrant DB                PostgreSQL
```

## Features

- **Multi-document ingestion** — PDF, DOCX, PPTX, HTML, Markdown, TXT
- **Hybrid retrieval** — Vector (Qdrant) + BM25 (PostgreSQL) with score fusion
- **Citation-based answers** — Inline `[n]` citations with source excerpts
- **Conversation memory** — History + automatic summarization
- **Role-based access** — Admin, Analyst, Viewer roles
- **Evaluation pipeline** — Offline metrics with sample datasets
- **Observability** — Prometheus metrics, Structlog JSON logging, LangSmith tracing
- **Agentic workflows** — LangGraph router → retrieval → answer → evaluate

## Quick Start

```bash
git clone https://github.com/satyazm/enterprise-rag-platform.git
cd enterprise-rag-platform
cp .env.example .env
# Add OPENAI_API_KEY to .env (optional — demo mode works without it)

docker compose up -d
```

Open http://localhost:3000 and sign in with:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | admin123 |
| Analyst | analyst@example.com | analyst123 |
| Viewer | viewer@example.com | viewer123 |

Demo users are created automatically on backend startup.

## Project Structure

```
enterprise-rag-platform/
├── backend/          # FastAPI + LangGraph RAG pipeline
├── frontend/         # Next.js enterprise UI
├── scripts/          # Ingestion, benchmark, dataset tools
├── evaluation/       # Datasets and experiment reports
├── tests/            # API, retrieval, graph, eval tests
└── docs/             # Architecture, deployment, API docs
```

## Development Roadmap

| Week | Focus |
|------|-------|
| 1 | Core RAG — ingestion, chunking, embeddings, basic chat, citations |
| 2 | Better retrieval — hybrid search, filters, reranking, query rewriting |
| 3 | Agentic layer — LangGraph workflow, memory, evaluation node |
| 4 | Production — auth, admin dashboard, Docker, CI/CD, observability |

## API

Interactive docs at http://localhost:8000/docs after starting the backend.

See [docs/api.md](docs/api.md) for the full reference.

## License

MIT
