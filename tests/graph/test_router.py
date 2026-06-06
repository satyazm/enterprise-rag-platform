from app.rag.agents.router_agent import classify_query


def test_classify_qa():
    assert classify_query("What is the refund policy?") == "qa"


def test_classify_summarize():
    assert classify_query("Summarize the onboarding docs") == "summarize"
