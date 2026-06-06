from sqlalchemy.ext.asyncio import AsyncSession

from app.rag.retrieval.filters import apply_filters, build_metadata_filters
from app.rag.retrieval.hybrid import HybridRetriever
from app.rag.retrieval.reranker import rerank


class RetrievalAgent:
    def __init__(self, db: AsyncSession):
        self.retriever = HybridRetriever(db)

    async def run(self, query: str, rewritten_query: str | None = None, filters: dict | None = None) -> list[dict]:
        search_query = rewritten_query or query
        metadata_filters = build_metadata_filters(**(filters or {}))
        results = await self.retriever.retrieve(search_query)
        results = apply_filters(results, metadata_filters)
        return rerank(search_query, results)
