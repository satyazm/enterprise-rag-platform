def evaluate_response(query: str, answer: str, contexts: list[str], ground_truth: str | None = None) -> dict:
    """Heuristic evaluation metrics for offline pipeline."""
    answer_lower = answer.lower()
    query_terms = set(query.lower().split())
    answer_terms = set(answer_lower.split())
    context_text = " ".join(contexts).lower()

    faithfulness = sum(1 for t in answer_terms if t in context_text) / max(len(answer_terms), 1)
    relevance = len(query_terms & answer_terms) / max(len(query_terms), 1)

    metrics = {
        "faithfulness": round(min(faithfulness, 1.0), 3),
        "answer_relevancy": round(min(relevance, 1.0), 3),
        "context_precision": round(min(len(contexts) / 5, 1.0), 3),
    }

    if ground_truth:
        gt_terms = set(ground_truth.lower().split())
        metrics["groundedness"] = round(len(gt_terms & answer_terms) / max(len(gt_terms), 1), 3)

    return metrics
