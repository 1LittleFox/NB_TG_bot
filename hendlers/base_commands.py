import buttons_lists as bl
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from instruction import HELP
from keyboards.simple_row import make_row_keyboard
from datetime import datetime

router = Router()


class Condition(StatesGroup):
    on_shift = State()
    choosing_categories = State()


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text="Привет, этот бот был создан специально для администраторов зала Невские медведи!",
        reply_markup=make_row_keyboard(bl.first_step)
    )
    await state.set_state(Condition.on_shift)


@router.message(Condition.on_shift, F.text == "Открыть смену")
async def cmd_pick(message: Message, state: FSMContext):
    await state.update_data(chosen_cmd=message.text.lower())
    time_now = datetime.now().strftime('%H:%M')
    added_text = "Начало смены в"
    await message.answer(
        text=f"{added_text} {time_now}",
        reply_markup=make_row_keyboard(bl.second_step)
    )
    await state.set_state(Condition.choosing_categories)


@router.message(Condition.on_shift, F.text == "Закрыть смену")
async def cmd_close_shift(message: Message, state: FSMContext):
    await state.update_data(chosen_cmd=message.text.lower())
    time_now = datetime.now().strftime('%H:%M')
    added_text = "Начало смены в"
    await message.answer(
        text=f"{added_text} {time_now}",
        reply_markup=make_row_keyboard(bl.second_step)
    )
    await state.set_state(Condition.choosing_categories)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        text=HELP
    )
