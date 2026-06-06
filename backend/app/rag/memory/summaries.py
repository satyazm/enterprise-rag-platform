from openai import AsyncOpenAI

from app.core.config import get_settings
from app.rag.prompts.summarization import CONVERSATION_SUMMARY_PROMPT

settings = get_settings()


async def summarize_conversation(messages: list[dict]) -> str:
    if not messages:
        return ""

    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in messages[-20:])
    if not settings.openai_api_key:
        return f"Conversation covering: {transcript[:200]}..."

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": CONVERSATION_SUMMARY_PROMPT},
            {"role": "user", "content": transcript},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
