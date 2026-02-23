import html 

def esc(s: str) -> str:
    return html.escape(s or "")

def render_topic_html(title: str, body: str) -> str:
    # Заголовок жирным, тело обычным
    return f"📘 <b>{esc(title)}</b>\n\n{esc(body)}"

def render_simple_html(title: str, simple: str) -> str:
    return f"🧠 <b>{esc(title)} - простыми словами</b>\n\n{esc(simple)}"

def render_example_html(title: str, code: str) -> str:
    # <pre> в Telegram не поддерживается, поэтому используем <code>
    # Telegram HTML понимает <code>...</code>. Для многострочного кода норм.
    return f"📌 <b>{esc(title)} - пример</b>\n\n<code>{esc(code)}</code>"

def render_search_results_html(query: str, items: list[dict]) -> str:
    lines = [f"🔎 <b>Поиск:</b> {esc(query)}\n"]
    for i, it in enumerate(items, 1):
        line = f"{i}. <b>{esc(it['topic_title'])}</b> <i>(раздел: {esc(it['section_title'])})</i>"
        if it.get("snippet_html"):
            # snippet_html содержит <b>..</b>, поэтому экранировать нельзя целиком.
            # Но он был построен без экранирования - значит мы экранируем исходники выше,
            # а в highlight вставили только <b>. Здесь делаем минимальную чистку:
            line += f"\n    {it['snippet_html']}"
        lines.append(line)
    return "\n".join(lines)

