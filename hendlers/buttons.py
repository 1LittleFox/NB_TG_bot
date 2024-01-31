import buttons_lists as bl
from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from keyboards.simple_row import make_row_keyboard


router = Router()


@router.message(Command("sell"))
async def cmd_start(message: Message):
    kb = [
        [
            KeyboardButton(text="Капучино"),
            KeyboardButton(text="Латте")
        ],

        [
            KeyboardButton(text="Американо"),
        ],

        [
            KeyboardButton(text="Раф"),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите напиток"
    )
    await message.answer("Какой напиток вы продали?", reply_markup=keyboard)


