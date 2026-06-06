import uuid

from app.core.config import get_settings
from app.rag.ingestion.chunking.metadata import enrich_chunk_metadata
from app.rag.ingestion.chunking.semantic import semantic_chunk
from app.rag.ingestion.embeddings import embed_texts
from app.rag.ingestion.loaders.docx import load_docx
from app.rag.ingestion.loaders.html import load_html
from app.rag.ingestion.loaders.pdf import load_pdf
from app.rag.ingestion.loaders.pptx import load_pptx
from app.rag.retrieval.vector_search import VectorSearch

settings = get_settings()

LOADERS = {
    "pdf": load_pdf,
    "docx": load_docx,
    "pptx": load_pptx,
    "html": load_html,
    "htm": load_html,
    "txt": lambda p: [{"content": open(p, encoding="utf-8", errors="ignore").read(), "metadata": {"source_type": "txt"}}],
    "md": lambda p: [{"content": open(p, encoding="utf-8", errors="ignore").read(), "metadata": {"source_type": "md"}}],
}


async def run_ingestion_pipeline(
    file_path: str,
    file_type: str,
    document_id: str,
    title: str,
) -> list[dict]:
    loader = LOADERS.get(file_type)
    if not loader:
        raise ValueError(f"No loader for file type: {file_type}")

    sections = loader(file_path)
    all_chunks: list[dict] = []
    chunk_index = 0

    for section in sections:
        chunks = semantic_chunk(section["content"], settings.chunk_size)
        for chunk_text in chunks:
            metadata = enrich_chunk_metadata(
                {**section.get("metadata", {})},
                chunk_index,
                document_id,
                title,
            )
            all_chunks.append({"content": chunk_text, "metadata": metadata, "chunk_index": chunk_index})
            chunk_index += 1

    texts = [c["content"] for c in all_chunks]
    embeddings = await embed_texts(texts)

    vector_search = VectorSearch()
    await vector_search.ensure_collection(len(embeddings[0]) if embeddings else 384)

    points = []
    for chunk, embedding in zip(all_chunks, embeddings):
        point_id = str(uuid.uuid4())
        chunk["qdrant_point_id"] = point_id
        points.append({
            "id": point_id,
            "vector": embedding,
            "payload": {
                "document_id": document_id,
                "document_title": title,
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"],
                **chunk["metadata"],
            },
        })

    if points:
        await vector_search.upsert(points)

    return all_chunks
