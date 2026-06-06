from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Conversation, Message, User
from app.rag.graph.workflow import build_rag_workflow
from app.rag.memory.conversation import get_conversation_history
from app.rag.memory.summaries import summarize_conversation


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_message(
        self,
        user: User,
        message: str,
        conversation_id: str | None = None,
    ) -> dict:
        if conversation_id:
            conv = await self.db.get(Conversation, UUID(conversation_id))
            if not conv or conv.user_id != user.id:
                conv = None
        else:
            conv = None

        if not conv:
            conv = Conversation(user_id=user.id, title=message[:80])
            self.db.add(conv)
            await self.db.flush()

        history = await get_conversation_history(self.db, str(conv.id))

        self.db.add(Message(conversation_id=conv.id, role="user", content=message))
        await self.db.flush()

        workflow = build_rag_workflow(self.db)
        result = await workflow.ainvoke({
            "query": message,
            "history": history,
            "rewritten_query": "",
            "route": "",
            "retrieved_chunks": [],
            "answer": "",
            "citations": [],
            "metrics": {},
            "trace_id": str(uuid4()),
            "messages": [],
        })

        assistant_msg = Message(
            conversation_id=conv.id,
            role="assistant",
            content=result["answer"],
            citations=result.get("citations", []),
            trace_id=result.get("trace_id"),
        )
        self.db.add(assistant_msg)

        conv.updated_at = datetime.now(timezone.utc)
        if len(history) >= 6:
            conv.summary = await summarize_conversation(history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": result["answer"]},
            ])

        await self.db.commit()

        return {
            "conversation_id": str(conv.id),
            "message": result["answer"],
            "citations": result.get("citations", []),
            "trace_id": result.get("trace_id"),
        }
