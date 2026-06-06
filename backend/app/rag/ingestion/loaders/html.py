from bs4 import BeautifulSoup


def load_html(path: str) -> list[dict]:
    with open(path, encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return [{"content": text, "metadata": {"source_type": "html"}}] if text else []
