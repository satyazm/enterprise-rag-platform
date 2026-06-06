import hashlib

from openai import AsyncOpenAI

from app.core.config import get_settings

settings = get_settings()
_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.openai_api_key or "sk-demo")
    return _client


async def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    if not settings.openai_api_key:
        return [_deterministic_embedding(t) for t in texts]

    client = _get_client()
    response = await client.embeddings.create(model=settings.embedding_model, input=texts)
    return [item.embedding for item in response.data]


def _deterministic_embedding(text: str, dim: int = 384) -> list[float]:
    """Fallback embedding for demo mode without API keys."""
    digest = hashlib.sha256(text.encode()).digest()
    values = []
    for i in range(dim):
        byte = digest[i % len(digest)]
        values.append((byte / 255.0) * 2 - 1)
    return values
