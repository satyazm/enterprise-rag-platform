from app.rag.evaluation.metrics import aggregate_metrics


def test_aggregate():
    runs = [{"faithfulness": 0.8, "answer_relevancy": 0.6}, {"faithfulness": 1.0, "answer_relevancy": 0.4}]
    result = aggregate_metrics(runs)
    assert result["faithfulness"] == 0.9
    assert result["answer_relevancy"] == 0.5
