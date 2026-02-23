
from logging_config import setup_logging
from middlewares.logging import LoggingMiddleware
from middlewares.errors import ErrorLoggingMiddleware

import asyncio
from aiogram import Bot, Dispatcher

from middlewares.ratelimit import RateLimitMiddleware
from middlewares.di import DIMiddleware

from storage.sqlite import SQLiteStorage
from settings import Settings

from handlers import (
    start_router, 
    content_router, 
    search_router, 
    errors_router, 
    favorites_router
    )

async def main():
    setup_logging(log_dir="logs")
    settings = Settings.load()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.update.middleware(RateLimitMiddleware(per_user_seconds=0.7))

    dp["storage"] = SQLiteStorage(settings.db_path)

    dp.update.middleware(ErrorLoggingMiddleware())
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(DIMiddleware())

    dp.include_router(start_router)
    dp.include_router(content_router)
    dp.include_router(search_router)
    dp.include_router(favorites_router)
    dp.include_router(errors_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

