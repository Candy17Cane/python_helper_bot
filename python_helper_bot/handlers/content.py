from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from services.content_service import get_topic, get_section
from services.render_service import render_topic_html, render_example_html, render_simple_html

from data.sections import SECTIONS
from data.content import CONTENT
from keyboards.content import section_menu_kb, topic_actions_kb
from storage.base import Storage
from typing import Optional, Tuple

router = Router()

def parse_cb(data: str) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    parts = (data or "").split(":")
    if len(parts) >= 4 and parts[1] == "v1":
        return parts[0], "v1", parts[2], parts[3]
    
    if len(parts) >= 3:
        return parts[0], None, parts[1], parts[2]
    
    return None, None, None, None

#  text: str, 
async def safe_edit_reply_markup(message, reply_markup=None):
    try:
        await message.edit_reply_markup(reply_markup=reply_markup)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise
            
async def safe_edit_text(message, text: str, reply_markup=None, parse_mode=None):
    try:
        await message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except TelegramBadRequest as e:
        # Telegram ругается если текст/клавиатура не изменилось
        if "message is not modified" not in str(e):
            raise

def _section_key_by_title(title: str) -> str | None:
    for k, v in SECTIONS.items():
        if v == title:
            return k
    return None

@router.message(lambda msg: msg.text in SECTIONS.values())
async def open_section(message: Message):
    section_key = _section_key_by_title(message.text)
    if not section_key:
        await message.answer("Раздел не найден. Нажми /start")
        return
    
    section = get_section(section_key)
    if not section_key:
        await message.answer("Раздел не найден. Нажми /start")
        return
    
    await message.answer(
        f"📚 Раздел: <b>{section['title']}</b>\n\nВыбери тему:",
        reply_markup=section_menu_kb(section_key),
        parse_mode="HTML"
    )

@router.callback_query(lambda c: c.data.startswith("topic:"))
async def open_topic(callback: CallbackQuery, storage: Storage):
    action, ver, section_key, topic_key = parse_cb(callback.data)

    topic = get_topic(section_key, topic_key)
    if not topic:
        await callback.answer("Тема не найдена", show_alert=True)
        return
    
    user_id = callback.from_user.id
    is_fav = storage.is_favorite(user_id, section_key, topic_key)

    await safe_edit_text(
        callback.message,
        render_topic_html(topic["title"], topic["text"]),
        reply_markup=topic_actions_kb(section_key, topic_key, is_fav),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("simple:"))
async def open_simple(callback: CallbackQuery, storage: Storage):
    action, ver, section_key, topic_key = parse_cb(callback.data)

    topic = get_topic(section_key, topic_key)
    if not topic:
        await callback.answer("Тема не найдема", show_alert=True)
        return
    
    user_id = callback.from_user.id
    is_fav = storage.is_favorite(user_id, section_key, topic_key)
    
    simple = topic.get("simple")
    if not simple:
        await callback.answer("Для этой темы нет обьяснения простыми словами.", show_alert=True)
        return
    
    await safe_edit_text(
        callback.message,
        render_simple_html(topic["title"], simple),
        reply_markup=topic_actions_kb(section_key, topic_key, is_fav),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("example:"))
async def open_example(callback: CallbackQuery, storage: Storage):
    action, ver, section_key, topic_key = parse_cb(callback.data)

    topic = get_topic(section_key, topic_key)
    if not topic:
        await callback.answer("Тема не найдена", show_alert=True)
        return
    
    user_id = callback.from_user.id
    is_fav = storage.is_favorite(user_id, section_key, topic_key)
    
    code = topic.get("example")
    if not code:
        await callback.answer("Для этой темы нет примера.", show_alert=True)
        return

    await safe_edit_text(
        callback.message,
        render_example_html(topic["title"], code),
        reply_markup=topic_actions_kb(section_key, topic_key, is_fav),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "back:main")
async def back_main(callback: CallbackQuery):
    await safe_edit_text(
        callback.message, 
        "⬅ Вернулся в главное меню. Выбери раздел (reply-кнопки ниже)."
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("back:section:"))
async def back_section(callback: CallbackQuery):
    parts = callback.data.split(":")
    if len(parts) >= 4 and parts[2] == "v1":
        section_key = parts[3]
    else:
        section_key = parts[2]

    section = get_section(section_key)
    if not section:
        await callback.answer("Раздел не найден", show_alert=True)
        return

    await safe_edit_text(
        callback.message,
        f"📚 Раздел: <b>{section['title']}</b>\n\nВыбери тему:",
        reply_markup=section_menu_kb(section_key),
        parse_mode="HTML"
    )
    await callback.answer()

def parse_fav(data: str):
    parts = data.split(":")
    if len(parts) >= 5 and parts[2] == "v1":
        return parts[1], parts[3], parts[4]
    return parts[1], parts[2], parts[3]

@router.callback_query(lambda c: c.data.startswith("fav:add:"))
async def fav_add(callback: CallbackQuery, storage: Storage):
    _, section_key, topic_key = parse_fav(callback.data)
    storage.add_favorite(callback.from_user.id, section_key, topic_key)
    await callback.answer("Добавлено в избранное ⭐")

@router.callback_query(lambda c: c.data.startswith("fav:del:"))
async def fav_del(callback: CallbackQuery, storage: Storage):
    _, _, section_key, topic_key = callback.data.split(":")
    storage.remove_favorite(callback.from_user.id, section_key, topic_key)
    await callback.answer("Убрано из избранного ❌")

@router.callback_query(lambda c: c.data.startswith("fav:toggle:"))
async def fav_toggle(callback: CallbackQuery, storage: Storage):
    parts = callback.data.split(":")

    if len(parts) >= 5 and parts[2] == "v1":
        section_key, topic_key = parts[3], parts[4]
    else:
        section_key, topic_key = parts[2], parts[3]
    
    user_id = callback.from_user.id

    if storage.is_favorite(user_id, section_key, topic_key):
        storage.remove_favorite(user_id, section_key, topic_key)
        new_state = False
        await callback.answer("Убрано из избранного ❌")
    else:
        storage.add_favorite(user_id, section_key, topic_key)
        new_state = True
        await callback.answer("Добавлено в избранное ⭐")

    await safe_edit_reply_markup(
        callback.message,
        reply_markup=topic_actions_kb(section_key, topic_key, new_state)
    )

