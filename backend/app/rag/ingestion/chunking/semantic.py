def semantic_chunk(text: str, chunk_size: int = 512) -> list[str]:
    """Paragraph-aware chunking for semantic coherence."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= chunk_size:
            current = f"{current}\n\n{para}".strip() if current else para
        else:
            if current:
                chunks.append(current)
            if len(para) > chunk_size:
                from app.rag.ingestion.chunking.recursive import recursive_chunk

                chunks.extend(recursive_chunk(para, chunk_size))
                current = ""
            else:
                current = para

    if current:
        chunks.append(current)
    return chunks
