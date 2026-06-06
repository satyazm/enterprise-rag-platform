from app.rag.agents.evaluator_agent import evaluate_response
from app.rag.evaluation.datasets import get_dataset
from app.rag.evaluation.metrics import aggregate_metrics


async def run_evaluation(dataset_name: str = "sample") -> dict:
    dataset = get_dataset(dataset_name)
    runs = []

    for item in dataset:
        metrics = evaluate_response(
            query=item["question"],
            answer=item["ground_truth"],
            contexts=item["contexts"],
            ground_truth=item["ground_truth"],
        )
        runs.append(metrics)

    aggregated = aggregate_metrics(runs)
    return {
        "dataset": dataset_name,
        "num_samples": len(dataset),
        "metrics": aggregated,
        "per_sample": runs,
    }
