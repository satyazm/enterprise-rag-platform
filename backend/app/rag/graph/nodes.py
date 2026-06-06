import uuid

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.rag.agents.answer_agent import AnswerAgent
from app.rag.agents.evaluator_agent import evaluate_response
from app.rag.agents.retrieval_agent import RetrievalAgent
from app.rag.agents.router_agent import classify_query
from app.rag.graph.state import RAGState

settings = get_settings()


async def router_node(state: RAGState, db) -> dict:
    route = classify_query(state["query"])
    rewritten = await _rewrite_query(state["query"])
    return {"route": route, "rewritten_query": rewritten, "trace_id": state.get("trace_id") or str(uuid.uuid4())}


async def retrieval_node(state: RAGState, db) -> dict:
    agent = RetrievalAgent(db)
    chunks = await agent.run(state["query"], state.get("rewritten_query"))
    return {"retrieved_chunks": chunks}


async def answer_node(state: RAGState, db) -> dict:
    agent = AnswerAgent()
    result = await agent.run(state["query"], state.get("retrieved_chunks", []), state.get("history"))
    return {"answer": result["answer"], "citations": result["citations"]}


async def evaluation_node(state: RAGState, db) -> dict:
    contexts = [c["content"] for c in state.get("retrieved_chunks", [])]
    metrics = evaluate_response(state["query"], state.get("answer", ""), contexts)
    return {"metrics": metrics}


async def _rewrite_query(query: str) -> str:
    if not settings.openai_api_key:
        return query
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": "Rewrite the user query for better document retrieval. Return only the rewritten query."},
            {"role": "user", "content": query},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or query
