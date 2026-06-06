from app.core.config import get_settings

settings = get_settings()


def rerank(query: str, results: list[dict], top_k: int | None = None) -> list[dict]:
    """Lightweight lexical reranker using query term overlap."""
    top_k = top_k or settings.final_top_k
    query_terms = set(query.lower().split())

    for r in results:
        content_terms = set(r["content"].lower().split())
        overlap = len(query_terms & content_terms) / max(len(query_terms), 1)
        base = r.get("hybrid_score", r.get("score", 0))
        r["rerank_score"] = base * 0.7 + overlap * 0.3

    return sorted(results, key=lambda x: x.get("rerank_score", 0), reverse=True)[:top_k]
