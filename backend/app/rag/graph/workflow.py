from functools import partial

from langgraph.graph import END, StateGraph

from app.rag.graph.edges import should_evaluate
from app.rag.graph.nodes import answer_node, evaluation_node, retrieval_node, router_node
from app.rag.graph.state import RAGState


def build_rag_workflow(db):
    graph = StateGraph(RAGState)

    graph.add_node("router", partial(router_node, db=db))
    graph.add_node("retrieval", partial(retrieval_node, db=db))
    graph.add_node("answer", partial(answer_node, db=db))
    graph.add_node("evaluate", partial(evaluation_node, db=db))

    graph.set_entry_point("router")
    graph.add_edge("router", "retrieval")
    graph.add_edge("retrieval", "answer")
    graph.add_conditional_edges("answer", should_evaluate, {"evaluate": "evaluate", "end": END})
    graph.add_edge("evaluate", END)

    return graph.compile()
