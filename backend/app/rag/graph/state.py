from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class RAGState(TypedDict):
    query: str
    rewritten_query: str
    route: str
    retrieved_chunks: list[dict]
    answer: str
    citations: list[dict]
    history: list[dict]
    metrics: dict
    trace_id: str
    messages: Annotated[list, add_messages]
