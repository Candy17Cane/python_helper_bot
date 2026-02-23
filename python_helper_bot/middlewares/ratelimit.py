from __future__ import annotations
import time
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, per_user_seconds: float = 0.7):
        self.per_user_seconds = per_user_seconds
        self._last: dict[tuple[int, str], float] = {}

    def _allowed(self, user_id: int, bucket: str) -> bool:
        now = time.monotonic()
        key = (user_id, bucket)
        last = self._last.get(key, 0.0)
        if now - last < self.per_user_seconds:
            return False
        self._last[key] = now
        return True
    
    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)
        
        if isinstance(event, CallbackQuery):
            if not self._allowed(user.id, "cb"):
                try:
                    await event.answer("Слишком часто 🙂", show_alert=False)
                except Exception:
                    pass
                return
        elif isinstance(event, Message):
            if not self._allowed(user.id, "msg"):
                return
            
        return await handler(event, data)
    
