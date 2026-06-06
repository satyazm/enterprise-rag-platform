def aggregate_metrics(runs: list[dict]) -> dict:
    if not runs:
        return {}
    keys = runs[0].keys()
    return {k: round(sum(r[k] for r in runs) / len(runs), 3) for k in keys if isinstance(runs[0][k], (int, float))}
