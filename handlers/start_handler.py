from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from adapters import user_db_adapter, model_db_adapter

from keyboards import start_keyboard

# create router for handling start bot
router_start = Router()

# create db adapter objects
user_db = user_db_adapter.UserDB()
model_db = model_db_adapter.ModelDB()


# handler to check bot is online or not
@router_start.message(Command('check'))
async def check_bot(message: Message):
    await message.answer("Bot is active")


# handling new user and create entity in DB
@router_start.message(Command('start'))
async def start_bot(message: Message):
    try:
        # try add user entity in db (users table)
        user_db.create_user(message.from_user.id, message.from_user.username)

        # if user added successfully, send message at the first start
        await message.answer('🚀 Давай начнем создание твоей новой модели \n',
                             reply_markup=start_keyboard.start_create_model_kb,
                             parse_mode="HTML")

    except Exception as e:
        # if user already exists
        # get all user models from db to create inline keyboard
        models = model_db.get_user_models(message.from_user.id)

        # send message with opportunity to choose model
        await message.answer('🚀 Выбери модель: \n',
                             reply_markup=start_keyboard.get_choose_model_kb(models),
                             parse_mode="HTML")

        print("Error", e)

    # delete `/start`
    await message.delete()




