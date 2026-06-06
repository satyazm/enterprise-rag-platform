import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user, require_role
from app.core.config import get_settings
from app.database.models import Document, DocumentStatus, User, UserRole
from app.database.postgres import get_db
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/documents", tags=["documents"])
settings = get_settings()


class DocumentResponse(BaseModel):
    id: str
    title: str
    filename: str
    file_type: str
    status: str

    class Config:
        from_attributes = True


@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(Document).order_by(Document.created_at.desc()))
    return [
        DocumentResponse(
            id=str(d.id), title=d.title, filename=d.filename, file_type=d.file_type, status=d.status.value
        )
        for d in result.scalars().all()
    ]


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    user: Annotated[User, Depends(require_role(UserRole.ADMIN, UserRole.ANALYST))],
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...),
):
    os.makedirs(settings.upload_dir, exist_ok=True)
    ext = os.path.splitext(file.filename or "")[1].lower()
    allowed = {".pdf", ".docx", ".pptx", ".html", ".htm", ".txt", ".md"}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    doc_id = uuid.uuid4()
    save_path = os.path.join(settings.upload_dir, f"{doc_id}{ext}")
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    document = Document(
        id=doc_id,
        title=file.filename or "Untitled",
        filename=file.filename or "untitled",
        file_type=ext.lstrip("."),
        status=DocumentStatus.PENDING,
        owner_id=user.id,
        metadata_json={"size_bytes": len(content)},
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    service = IngestionService(db)
    await service.ingest_document(document, save_path)

    return DocumentResponse(
        id=str(document.id),
        title=document.title,
        filename=document.filename,
        file_type=document.file_type,
        status=document.status.value,
    )


@router.delete("/{document_id}")
async def delete_document(
    document_id: uuid.UUID,
    user: Annotated[User, Depends(require_role(UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(document)
    await db.commit()
    return {"status": "deleted"}
