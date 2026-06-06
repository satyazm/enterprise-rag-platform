import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.database.models import Conversation, Message, User
from app.database.postgres import get_db
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class Citation(BaseModel):
    document_id: str
    document_title: str
    chunk_index: int
    excerpt: str
    score: float


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    citations: list[Citation]
    trace_id: str | None = None


class ConversationResponse(BaseModel):
    id: str
    title: str
    updated_at: str


class MessageResponse(BaseModel):
    role: str
    content: str
    citations: list
    created_at: str


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    service = ChatService(db)
    result = await service.process_message(
        user=user,
        message=payload.message,
        conversation_id=payload.conversation_id,
    )
    return ChatResponse(**result)


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
    )
    return [
        ConversationResponse(id=str(c.id), title=c.title, updated_at=c.updated_at.isoformat())
        for c in result.scalars().all()
    ]


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_messages(
    conversation_id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    conv = await db.get(Conversation, conversation_id)
    if not conv or conv.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    result = await db.execute(
        select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    )
    return [
        MessageResponse(
            role=m.role,
            content=m.content,
            citations=m.citations or [],
            created_at=m.created_at.isoformat(),
        )
        for m in result.scalars().all()
    ]
