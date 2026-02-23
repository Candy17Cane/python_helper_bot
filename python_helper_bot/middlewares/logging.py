from __future__ import annotations

import logging
import time
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger("bot.update")

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        user_id = getattr(user, "id", None)
        username = getattr(user, "username", None)

        start = time.perf_counter()

        if isinstance(event, Message):
            text = (event.text or event.caption or "").replace("\n", "\\n")
            logger.info(f"Message | user={user_id} @{username} | text='{text[:200]}'")
        elif isinstance(event, CallbackQuery):
            cb = (event.data or "").replace("\n", "\\n")
            logger.info(f"Callback | user={user_id} @{username} | data='{cb[:300]}'")
        else:
            logger.info(f"{type(event).__name__} | user={user_id} @{username}")

        try:
            result = await handler(event, data)
            return result
        finally: 
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info(f"Handler | user={user_id} | {type(event).__name__} | {elapsed_ms:.1f}ms")


    
