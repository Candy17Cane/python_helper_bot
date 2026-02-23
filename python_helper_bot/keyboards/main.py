from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.sections import SECTIONS

def main_menu() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=name)] for name in SECTIONS.values()]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


