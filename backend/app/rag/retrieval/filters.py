def build_metadata_filters(
    document_ids: list[str] | None = None,
    source_type: str | None = None,
) -> dict:
    filters: dict = {}
    if document_ids:
        filters["document_ids"] = document_ids
    if source_type:
        filters["source_type"] = source_type
    return filters


def apply_filters(results: list[dict], filters: dict) -> list[dict]:
    if not filters:
        return results

    filtered = results
    if doc_ids := filters.get("document_ids"):
        filtered = [r for r in filtered if r.get("document_id") in doc_ids]
    if source_type := filters.get("source_type"):
        filtered = [r for r in filtered if r.get("source_type") == source_type]
    return filtered
