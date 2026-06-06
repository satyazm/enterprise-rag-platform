import re

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.rag.prompts.citation import CITATION_INSTRUCTION
from app.rag.prompts.system import SYSTEM_PROMPT

settings = get_settings()


def _format_context(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[{i}] {chunk.get('document_title', 'Unknown')} (chunk {chunk.get('chunk_index', 0)})\n"
            f"{chunk['content']}"
        )
    return "\n\n".join(parts)


def _extract_citations(answer: str, chunks: list[dict]) -> list[dict]:
    cited_indices = {int(m) for m in re.findall(r"\[(\d+)\]", answer)}
    citations = []
    for idx in sorted(cited_indices):
        if 1 <= idx <= len(chunks):
            c = chunks[idx - 1]
            citations.append({
                "document_id": c.get("document_id", ""),
                "document_title": c.get("document_title", "Unknown"),
                "chunk_index": c.get("chunk_index", 0),
                "excerpt": c["content"][:300],
                "score": c.get("rerank_score", c.get("hybrid_score", 0)),
            })
    if not citations and chunks:
        for c in chunks[:3]:
            citations.append({
                "document_id": c.get("document_id", ""),
                "document_title": c.get("document_title", "Unknown"),
                "chunk_index": c.get("chunk_index", 0),
                "excerpt": c["content"][:300],
                "score": c.get("rerank_score", c.get("hybrid_score", 0)),
            })
    return citations


class AnswerAgent:
    async def run(self, query: str, chunks: list[dict], history: list[dict] | None = None) -> dict:
        context = _format_context(chunks)
        messages = [
            {"role": "system", "content": f"{SYSTEM_PROMPT}\n\n{CITATION_INSTRUCTION}"},
        ]
        if history:
            messages.extend(history[-6:])
        messages.append({
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}",
        })

        if not settings.openai_api_key:
            answer = self._demo_answer(query, chunks)
        else:
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                temperature=0.2,
            )
            answer = response.choices[0].message.content or ""

        return {
            "answer": answer,
            "citations": _extract_citations(answer, chunks),
        }

    def _demo_answer(self, query: str, chunks: list[dict]) -> str:
        if not chunks:
            return "I don't have relevant documents indexed yet. Please upload documents first."
        top = chunks[0]
        return (
            f"Based on **{top.get('document_title', 'the knowledge base')}**, "
            f"here is what I found regarding your question:\n\n"
            f"{top['content'][:500]}...\n\n"
            f"[1] Source: {top.get('document_title', 'Unknown')}"
        )
