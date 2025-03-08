from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from keyboards import menu_keyboard

router_menu = Router()


@router_menu.message(Command('menu'))
async def open_menu(message: Message, state: FSMContext):
    await state.set_state(None)

    await message.answer("<b>Что хочешь посмотреть?</b>",
                         reply_markup=menu_keyboard.menu_kb,
                         parse_mode="HTML")

    await message.delete()


@router_menu.callback_query(F.data.startswith('menu'))
async def open_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)

    await callback.message.edit_text("<b>Что хочешь посмотреть?</b>",
                         reply_markup=menu_keyboard.menu_kb,
                         parse_mode="HTML")

    await callback.answer()






