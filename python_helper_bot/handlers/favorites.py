from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from storage.base import Storage
from data.content import CONTENT
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

def favorites_kb(favs: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    rows = []
    for section_key, topic_key in favs[:20]:
        topic = CONTENT.get(section_key, {}).get("topics", {}).get(topic_key)
        if not topic:
            continue
        rows.append([InlineKeyboardButton(
            text=f"{topic['title']}",
            callback_data=f"topic:{section_key}:{topic_key}"
        )])
    rows.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

@router.message(Command("favorites"))
async def show_favorites(message: Message, storage: Storage):
    favs = storage.list_favorites(message.from_user.id)
    if not favs:
        await message.answer("Избранное пусто. Добавь темы через ⭐")
        return
    await message.answer("⭐ Твое избранное:", reply_markup=favorites_kb(favs))

