from rank_bm25 import BM25Okapi

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import DocumentChunk


class BM25Search:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._corpus: list[dict] = []
        self._bm25: BM25Okapi | None = None

    async def build_index(self) -> None:
        result = await self.db.execute(select(DocumentChunk))
        chunks = result.scalars().all()
        self._corpus = [
            {
                "document_id": str(c.document_id),
                "chunk_index": c.chunk_index,
                "content": c.content,
                "metadata": c.metadata_json or {},
            }
            for c in chunks
        ]
        tokenized = [doc["content"].lower().split() for doc in self._corpus]
        self._bm25 = BM25Okapi(tokenized) if tokenized else None

    async def search(self, query: str, top_k: int = 20) -> list[dict]:
        if not self._bm25:
            await self.build_index()
        if not self._bm25 or not self._corpus:
            return []

        scores = self._bm25.get_scores(query.lower().split())
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for idx, score in ranked:
            if score <= 0:
                continue
            doc = self._corpus[idx]
            results.append({
                "document_id": doc["document_id"],
                "document_title": doc["metadata"].get("document_title", "Unknown"),
                "chunk_index": doc["chunk_index"],
                "content": doc["content"],
                "score": float(score),
                "source": "bm25",
            })
        return results
