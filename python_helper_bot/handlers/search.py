from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from data.sections import SECTIONS
from keyboards.content import search_results_kb
from services.content_service import search as service_search
from services.render_service import render_search_results_html

router = Router()

def _is_section_button(text: str) -> bool:
    return text in SECTIONS.values()

def _looks_like_search(text: str) -> bool:
    if not text:
        return False
    t = text.strip()
    if t.startswith("/"):
        return False
    # не ищем по слишком короткому мусору
    return len(t) >= 2

@router.message(Command("search"))
async def cmd_search(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "Напиши так:\n\n"
            "<code>/search инкапсуляция</code>\n"
            "<code>/search class</code>\n",
            parse_mode="HTML"
        )
        return

    query = parts[1].strip()
    found = service_search(query, limit=10)

    if not found:
        await message.answer(f"Ничего не нашёл по запросу: <b>{query}</b>", parse_mode="HTML")
        return

    # сервис вернул TopicRef, рендерим HTML
    # render_search_results_html ожидает list[dict] в моей ранней версии,
    # поэтому сделаем лёгкую адаптацию:
    items = [
        {
            "topic_title": x.topic_title,
            "section_title": x.section_title,
            "snippet_html": x.snippet_html,
        }
        for x in found
    ]

    await message.answer(
        render_search_results_html(query, items),
        reply_markup=search_results_kb(found),
        parse_mode="HTML"
    )

@router.message()
async def smart_search_fallback(message: Message):
    if _is_section_button(message.text):
        return
    if not _looks_like_search(message.text):
        return

    query = message.text.strip()
    found = service_search(query, limit=7)

    if not found:
        return

    items = [
        {
            "topic_title": x.topic_title,
            "section_title": x.section_title,
            "snippet_html": x.snippet_html,
        }
        for x in found
    ]

    await message.answer(
        render_search_results_html(query, items),
        reply_markup=search_results_kb(found),
        parse_mode="HTML"
    )
