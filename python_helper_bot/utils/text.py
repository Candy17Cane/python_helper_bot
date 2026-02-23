import re

STOP_WORDS = {
    "и", "в", "во", "на", "по", "для", "это", "что", "как", "а", "но", "или",
    "the", "a", "an", "to", "of", "in", "on", "for", "and", "or"
}

def norm(text: str) -> str:
    return (text or "").lower().strip()

def tokens(text: str) -> list[str]:
    # берем слова/числа/подчеркивания
    words = re.findall(r"[a-za-я0-9_]+", norm(text))
    return [w for w in words if len(w) >= 2 and w not in STOP_WORDS]

def highlight(text: str, query_tokens: list[str], limit: int = 140) -> str:
    """
    Делаем короткий сниппет и подсвечиваем совпадения.
    в HTML-рендер подсветка будет <b>..</b>.
    """
    if not text:
        return ""
    
    low = norm(text)
    idx = None
    for t in query_tokens:
        pos = low.find(t)
        if pos != -1 and (idx is None or pos < idx):
            idx = pos

    if idx is None:
        snippet = text[:limit]
    else:
        start = max(0, idx - 50)
        snippet = text[start:start + limit]

    # Оборачиваем найденные токены в <b>..<b/> (не экранируем тут!)
    # Экранирование будет на уровне render_service.
    for t in sorted(set(query_tokens), key=len, reverse=True):
        snippet = re.sub(rf"({re.escape(t)})", r"<b>\1</b>", snippet, flags=re.IGNORECASE)

    if len(text) > len(snippet):
        snippet += "..."
    return snippet

