from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main import main_menu

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет 👋\n\n"
        "Я - справочник по python.\n"
        "Выбери раздел:",
        reply_markup=main_menu()
    )
