from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Message


async def get_conversation_history(db: AsyncSession, conversation_id: str, limit: int = 10) -> list[dict]:
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = list(reversed(result.scalars().all()))
    return [{"role": m.role, "content": m.content} for m in messages]
