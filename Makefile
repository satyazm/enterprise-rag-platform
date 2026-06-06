.PHONY: up down build logs test ingest benchmark eval migrate seed

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec backend python -m scripts.seed_users

ingest:
	python scripts/ingest_documents.py --path evaluation/datasets/sample_docs

benchmark:
	python scripts/benchmark.py

eval:
	python scripts/create_dataset.py && docker compose exec backend python -m app.rag.evaluation.ragas_eval

test:
	cd backend && pytest ../tests -v

backend-dev:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend-dev:
	cd frontend && npm run dev
