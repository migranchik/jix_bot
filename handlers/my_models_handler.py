from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import start_keyboard

from adapters import model_db_adapter

# create router for handling generate image
router_my_models = Router()

# create db adapter objects
model_db = model_db_adapter.ModelDB()


# handling the click to `my models`
@router_my_models.callback_query(F.data.startswith('my_models'))
async def open_my_models(callback: CallbackQuery):
    models = model_db.get_user_models(callback.from_user.id)

    # send message with opportunity to choose model
    await callback.message.edit_text('🚀 Выбери модель: \n',
                                     reply_markup=start_keyboard.get_choose_model_kb(models),
                                     parse_mode="HTML")


