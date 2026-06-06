def enrich_chunk_metadata(base: dict, chunk_index: int, document_id: str, title: str) -> dict:
    return {
        **base,
        "chunk_index": chunk_index,
        "document_id": document_id,
        "document_title": title,
    }
