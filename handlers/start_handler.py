from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from adapters import user_db_adapter

from keyboards import start_keyboard

router_start = Router()
user_db_adapter = user_db_adapter.UserDB()


@router_start.message(Command('check'))
async def check_bot(message: Message):
    await message.answer("Бот работает")


@router_start.message(Command('start'))
async def start_bot(message: Message):
    try:
        user_db_adapter.create_user(message.from_user.id, message.from_user.username)

        await message.answer('🚀 Давай начнем создание твоей новой модели \n',
                             reply_markup=start_keyboard.continue_to_menu_kb,
                             parse_mode="HTML")

    except Exception as e:
        await message.answer('<i>MENU</i>',
                             parse_mode="HTML")

        print("Error", e)

    await message.delete()




