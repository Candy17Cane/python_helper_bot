from aiogram import BaseMiddleware

class DIMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        dp = data.get("dispetcher")
        if dp and "storage" in dp:
            data["storage"] = dp["storage"]
        return await handler(event, data)