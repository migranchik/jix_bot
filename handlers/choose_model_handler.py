from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import general_keyboards

from adapters import model_db_adapter, learn_photo_db_adapter

# create router for handling choosing model
router_choose_model = Router()

# create db adapter objects
model_db = model_db_adapter.ModelDB()
learn_photo_db = learn_photo_db_adapter.LearnPhotoDB()


# handling the click to model (choosing model)
@router_choose_model.callback_query(F.data.startswith('chose_model_'))
async def choose_model(callback: CallbackQuery, state: FSMContext):
    # take model_id from inline button which was selected
    model_id = callback.data.split('_')[2]

    model = model_db.get_model(user_id=callback.from_user.id,
                               model_id=model_id)
    model_name = model[2]

    # save selected model_id in bot storage
    await state.update_data(model_id=model_id)

    # send message to user about readiness receive text prompt
    await callback.message.edit_text(f"✅ Готово! Теперь используется модель: <b>{model_name}</b>. \n\n"
                                     f"📸 Что дальше? \n"
                                     f"Вернитесь обратно в меню по кнопке «◀️ Назад»",
                                     reply_markup=general_keyboards.back_to_menu_kb,
                                     parse_mode="HTML")

    # turn off loading animation of inline button
    await callback.answer()


# handling any text message if model is selected and start generate with AstriaAPI
# @router_generate_image.message(F.text, GenerateState.waiting_prompt)
# async def start_generating(message: Message, state: FSMContext):
#     # get all data from bot storage
#     data = await state.get_data()
#
#     # notify user about starting generation image
#     await message.answer(f'⏳ Генерирую изображение с моделью {data["model_id"]}, пожалуйста, подождите...')
#
#     # do request to Astria API, which runs image generation
#     astria_api.create_prompt(model_id=data["model_id"],
#                              user_id=message.from_user.id,
#                              prompt_text=message.text)

