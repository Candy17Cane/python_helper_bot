from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Sequence
from services.content_service import TopicRef
from data.content import CONTENT

def section_menu_kb(section_key: str) -> InlineKeyboardMarkup:
    topics = CONTENT[section_key]["topics"]
    rows = [
        [InlineKeyboardButton(text=t["title"], callback_data=f"topic:v1:{section_key}:{topic_key}")]
        for topic_key, t in topics.items()
    ]
    rows.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back:main:v1")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def topic_actions_kb(section_key: str, topic_key: str, is_fav: bool) -> InlineKeyboardMarkup:
    fav_text = "✅ В избранном" if is_fav else "⭐ В избранное"
    fav_cb = f"fav:toggle:{section_key}:{topic_key}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 Простыми словами", callback_data=f"simple:v1:{section_key}:{topic_key}")],
            [InlineKeyboardButton(text="📌 Пример", callback_data=f"example:v1:{section_key}:{topic_key}")],
            [InlineKeyboardButton(text=fav_text, callback_data=f"fav:toggle:v1:{section_key}:{topic_key}")],
            [InlineKeyboardButton(text="⬅ К темам", callback_data=f"back:section:v1:{section_key}")],
        ]
    )

def search_results_kb(found: Sequence[TopicRef]) -> InlineKeyboardMarkup:
    rows = []
    for item in found[:10]:
        rows.append([
            InlineKeyboardButton(
                text=f"{item.topic_title} • {item.section_title}",
                callback_data=f"topic:{item.section_key}:{item.topic_key}"
            )
        ])

    rows.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

