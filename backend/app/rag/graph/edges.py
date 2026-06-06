from app.rag.graph.state import RAGState


def should_evaluate(state: RAGState) -> str:
    if state.get("route") == "evaluate":
        return "evaluate"
    return "end"
