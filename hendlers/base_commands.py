import buttons_lists as bl
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from instruction import HELP
from keyboards.simple_row import make_row_keyboard
from datetime import datetime

"""Подумать над вводом количества товара"""
router = Router()


class Condition(StatesGroup):
    on_shift = State()
    off_shift = State()
    choosing_categories = State()
    choosing_hot_drinks = State()


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text="Привет, этот бот был создан специально для администраторов зала Невские медведи!",
        reply_markup=make_row_keyboard(bl.first_step)
    )
    await state.set_state(Condition.off_shift)


@router.message(Condition.off_shift, F.text == "Открыть смену")
async def cmd_pick(message: Message, state: FSMContext):
    await state.update_data(chosen_cmd=message.text.lower())
    time_now = datetime.now().strftime('%H:%M')
    added_text = "Начало смены в"
    await message.answer(
        text=f"{added_text} {time_now}",
        reply_markup=make_row_keyboard(bl.second_step)
    )
    await state.set_state(Condition.on_shift)


@router.message(Condition.on_shift, F.text == "Закрыть смену")
async def cmd_close_shift(message: Message, state: FSMContext):
    await state.update_data(chosen_cmd=message.text.lower())
    time_now = datetime.now().strftime('%H:%M')
    added_text = "Закрытие смены в"
    await message.answer(
        text=f"{added_text} {time_now}",
        reply_markup=make_row_keyboard(bl.first_step)
    )
    await state.set_state(Condition.off_shift)


@router.message(Condition.on_shift, F.text == "Продажа")
async def cmd_sell(message: Message, state: FSMContext):
    await state.update_data(chosen_cmd=message.text.lower())
    await message.answer(
        text="выберите категорию проданного товара",
        reply_markup=make_row_keyboard(bl.categories)
        )
    await state.set_state(Condition.choosing_categories)


@router.message(Condition.choosing_categories, F.text == "Горячие напитки")
async def hot_drinks(message: Message, state: FSMContext):
    await state.update_data(chosen_cmd=message.text.lower())
    await message.answer(
        text="Какой напиток вы продали?",
        reply_markup=make_row_keyboard(bl.hot_drinks)
        )
    await state.set_state(Condition.choosing_hot_drinks)


@router.message(Condition.choosing_hot_drinks, F.text.in_(bl.hot_drinks))
async def sell_hot_drinks(message: Message, state: FSMContext):
    await state.update_data(chosen_cmd=message.text.lower())
    await message.answer(
        text="Напиток внесен в чек",
        reply_markup=make_row_keyboard(bl.list_after_chosen)
    )
    if F.text == "Закрыть чек":
        await state.set_state(Condition.on_shift),
        await message.answer(
            text="Чек закрыт",
            reply_markup=make_row_keyboard(bl.categories)
        )
    else:
        await state.set_state(Condition.choosing_categories)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        text=HELP
    )
