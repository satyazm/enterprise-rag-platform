import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, make_asgi_app

from app.api import admin, auth, chat, documents, health
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.database.postgres import init_db

if os.getenv("LANGCHAIN_TRACING_V2", "").lower() == "true":
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")

REQUEST_COUNT = Counter("rag_requests_total", "Total API requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("rag_request_latency_seconds", "Request latency", ["endpoint"])

setup_logging()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = settings.api_prefix
app.include_router(health.router, prefix=api)
app.include_router(auth.router, prefix=api)
app.include_router(documents.router, prefix=api)
app.include_router(chat.router, prefix=api)
app.include_router(admin.router, prefix=api)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
