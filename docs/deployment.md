# Deployment

## Docker Compose (Recommended)

```bash
cp .env.example .env
# Add your OPENAI_API_KEY
make up
make seed
make ingest
```

Services:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Metrics: http://localhost:8000/metrics

## Local Development

```bash
# Start infrastructure
docker compose up -d postgres qdrant

# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

## Environment Variables

See `.env.example` for all configuration options.
