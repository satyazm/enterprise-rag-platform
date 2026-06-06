from pypdf import PdfReader


def load_pdf(path: str) -> list[dict]:
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"content": text, "metadata": {"page": i + 1, "source_type": "pdf"}})
    return pages
