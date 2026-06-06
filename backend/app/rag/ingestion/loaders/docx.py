from docx import Document as DocxDocument


def load_docx(path: str) -> list[dict]:
    doc = DocxDocument(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    content = "\n\n".join(paragraphs)
    return [{"content": content, "metadata": {"source_type": "docx"}}] if content else []
