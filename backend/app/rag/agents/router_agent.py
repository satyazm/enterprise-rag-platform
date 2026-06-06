def classify_query(query: str) -> str:
    """Route query to appropriate workflow path."""
    q = query.lower()
    if any(w in q for w in ("summarize", "overview", "tl;dr")):
        return "summarize"
    if any(w in q for w in ("compare", "difference", "vs")):
        return "compare"
    if any(w in q for w in ("evaluate", "benchmark", "score")):
        return "evaluate"
    return "qa"
