from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import general_keyboards

from adapters import user_db_adapter, model_db_adapter

from utils import format

# create router for handling generate image
router_profile = Router()

# create db adapter objects
user_db = user_db_adapter.UserDB()
model_db = model_db_adapter.ModelDB()


# handling the click to profile
@router_profile.callback_query(F.data.startswith('profile'))
async def open_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id_formatted = format.format_user_id(str(callback.from_user.id))
    tokens = user_db.get_user_tokens(callback.from_user.id)

    model_id = data.get("model_id")
    model_name = ''
    if model_id is None:
        model_name = "модель не выбрана"
    else:
        model = model_db.get_model(user_id=callback.from_user.id,
                                   model_id=model_id)
        model_name = model[2]

    model_count = len(model_db.get_user_models(callback.from_user.id))

    await callback.message.edit_text(f"📅 <b>Ваш профиль</b> \n\n"
                                     f"• <b>Мой Id</b>: {user_id_formatted} \n"
                                     f"• <b>Количество токенов:</b> {tokens}\n"
                                     f"• <b>Выбранная модель:</b> <b>{model_name}</b> \n"
                                     f"• <b>Количество созданных моделей:</b> {model_count} \n"
                                     f"✨ Спасибо, что пользуетесь нашим сервисом! 🛠",
                                     reply_markup=general_keyboards.back_to_menu_kb,
                                     parse_mode="HTML")


