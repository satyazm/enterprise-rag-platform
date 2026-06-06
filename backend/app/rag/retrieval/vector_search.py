from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import get_settings

settings = get_settings()


class VectorSearch:
    def __init__(self):
        self.client = AsyncQdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.collection = settings.qdrant_collection

    async def ensure_collection(self, vector_size: int) -> None:
        collections = await self.client.get_collections()
        names = [c.name for c in collections.collections]
        if self.collection not in names:
            await self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    async def upsert(self, points: list[dict]) -> None:
        await self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(id=p["id"], vector=p["vector"], payload=p["payload"])
                for p in points
            ],
        )

    async def search(self, query_vector: list[float], top_k: int = 20, filters: dict | None = None) -> list[dict]:
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        qdrant_filter = None
        if filters and filters.get("document_id"):
            qdrant_filter = Filter(
                must=[FieldCondition(key="document_id", match=MatchValue(value=filters["document_id"]))]
            )

        results = await self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=top_k,
            query_filter=qdrant_filter,
        )
        return [
            {
                "document_id": r.payload.get("document_id"),
                "document_title": r.payload.get("document_title"),
                "chunk_index": r.payload.get("chunk_index"),
                "content": r.payload.get("content"),
                "score": float(r.score),
                "source": "vector",
            }
            for r in results
        ]
