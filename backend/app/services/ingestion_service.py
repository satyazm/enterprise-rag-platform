from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Document, DocumentChunk, DocumentStatus
from app.rag.ingestion.pipeline import run_ingestion_pipeline


class IngestionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_document(self, document: Document, file_path: str) -> None:
        document.status = DocumentStatus.PROCESSING
        await self.db.commit()

        try:
            chunks = await run_ingestion_pipeline(
                file_path=file_path,
                file_type=document.file_type,
                document_id=str(document.id),
                title=document.title,
            )

            for chunk in chunks:
                self.db.add(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=chunk["chunk_index"],
                        content=chunk["content"],
                        metadata_json=chunk["metadata"],
                        qdrant_point_id=chunk.get("qdrant_point_id"),
                    )
                )

            document.status = DocumentStatus.INDEXED
            document.indexed_at = datetime.now(timezone.utc)
            await self.db.commit()
        except Exception:
            document.status = DocumentStatus.FAILED
            await self.db.commit()
            raise
