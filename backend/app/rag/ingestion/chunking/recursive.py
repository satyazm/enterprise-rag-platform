def recursive_chunk(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            break_point = text.rfind("\n", start, end)
            if break_point == -1:
                break_point = text.rfind(" ", start, end)
            if break_point > start:
                end = break_point
        chunks.append(text[start:end].strip())
        start = max(end - overlap, start + 1)
    return [c for c in chunks if c]
