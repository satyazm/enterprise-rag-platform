from langgraph.graph import END, StateGraph

from app.rag.graph.edges import should_evaluate
from app.rag.graph.nodes import answer_node, evaluation_node, retrieval_node, router_node
from app.rag.graph.state import RAGState


def build_rag_workflow(db):
    graph = StateGraph(RAGState)

    async def router(state: RAGState):
        return await router_node(state, db)

    async def retrieval(state: RAGState):
        return await retrieval_node(state, db)

    async def generate_answer(state: RAGState):
        return await answer_node(state, db)

    async def run_evaluation(state: RAGState):
        return await evaluation_node(state, db)

    graph.add_node("router", router)
    graph.add_node("retrieval", retrieval)
    graph.add_node("generate_answer", generate_answer)
    graph.add_node("run_evaluation", run_evaluation)

    graph.set_entry_point("router")
    graph.add_edge("router", "retrieval")
    graph.add_edge("retrieval", "generate_answer")
    graph.add_conditional_edges("generate_answer", should_evaluate, {"evaluate": "run_evaluation", "end": END})
    graph.add_edge("run_evaluation", END)

    return graph.compile()
