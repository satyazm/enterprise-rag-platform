# Architecture

## Overview

Enterprise RAG Platform is an internal AI knowledge system with multi-document ingestion, hybrid retrieval, citation-based answers, and agentic workflows.

## Components

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React, Tailwind |
| API | FastAPI, Pydantic v2 |
| Vector DB | Qdrant |
| Relational DB | PostgreSQL |
| Orchestration | LangGraph |
| LLM | OpenAI GPT-4o-mini / Gemini |
| Observability | Prometheus, LangSmith, Structlog |

## Data Flow

1. Documents uploaded via API → ingestion pipeline (load → chunk → embed → index)
2. User query → LangGraph workflow (router → retrieval → answer → optional eval)
3. Hybrid retrieval fuses Qdrant vector search + PostgreSQL BM25
4. Reranker scores results, answer agent generates cited response
5. Conversation memory persisted with optional summarization

## Security

- JWT authentication with role-based access (admin, analyst, viewer)
- Audit logging for admin actions
- Document access controlled by role permissions
