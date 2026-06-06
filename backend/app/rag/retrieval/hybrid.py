from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.rag.ingestion.embeddings import embed_texts
from app.rag.retrieval.bm25 import BM25Search
from app.rag.retrieval.vector_search import VectorSearch

settings = get_settings()


def _normalize_scores(results: list[dict]) -> list[dict]:
    if not results:
        return []
    scores = [r["score"] for r in results]
    min_s, max_s = min(scores), max(scores)
    span = max_s - min_s or 1.0
    for r in results:
        r["norm_score"] = (r["score"] - min_s) / span
    return results


def _fuse_results(vector_results: list[dict], bm25_results: list[dict], alpha: float) -> list[dict]:
    combined: dict[str, dict] = {}

    for r in _normalize_scores(vector_results):
        key = f"{r['document_id']}:{r['chunk_index']}"
        combined[key] = {**r, "hybrid_score": alpha * r["norm_score"]}

    for r in _normalize_scores(bm25_results):
        key = f"{r['document_id']}:{r['chunk_index']}"
        if key in combined:
            combined[key]["hybrid_score"] += (1 - alpha) * r["norm_score"]
        else:
            combined[key] = {**r, "hybrid_score": (1 - alpha) * r["norm_score"]}

    return sorted(combined.values(), key=lambda x: x["hybrid_score"], reverse=True)


class HybridRetriever:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vector = VectorSearch()
        self.bm25 = BM25Search(db)

    async def retrieve(self, query: str, top_k: int | None = None, filters: dict | None = None) -> list[dict]:
        top_k = top_k or settings.rerank_top_k

        vector_results: list[dict] = []
        try:
            query_embedding = (await embed_texts([query]))[0]
            vector_results = await self.vector.search(query_embedding, top_k=top_k, filters=filters)
        except Exception:
            pass  # fall back to BM25-only if Qdrant or embeddings fail

        bm25_results = await self.bm25.search(query, top_k=top_k)

        if vector_results and bm25_results:
            return _fuse_results(vector_results, bm25_results, settings.hybrid_alpha)
        return vector_results or bm25_results
