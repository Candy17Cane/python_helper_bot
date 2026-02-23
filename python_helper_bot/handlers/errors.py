import logging
from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()
logger = logging.getLogger("errors")

@router.error()
async def global_error_handler(event: ErrorEvent):
    logger.exception("Unhandled error:", exc_info=event.exception)

