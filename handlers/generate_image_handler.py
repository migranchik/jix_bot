from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot import astria_api

from adapters import model_db_adapter, learn_photo_db_adapter
from states.GenerateState import GenerateState

# create router for handling generate image
router_generate_image = Router()

# create db adapter objects
model_db = model_db_adapter.ModelDB()
learn_photo_db = learn_photo_db_adapter.LearnPhotoDB()


# handling the click to model (choosing model)
@router_generate_image.callback_query(F.data.startswith('chose_model_'))
async def start_generating(callback: CallbackQuery, state: FSMContext):
    # take model_id from inline button which was selected
    model_id = callback.data.split('_')[2]

    # save selected model_id in bot storage
    await state.update_data(model_id=model_id)

    # send message to user about readiness receive text prompt
    await callback.message.answer(f"✅ Готово! Теперь используется модель: {model_id}. \n\n"
                                  f"📸 Что дальше? \n"
                                  f"Напиши максимально подробный текст для генерации, чтобы Jix сам придумал похожий образ!")

    # set waiting prompt text state
    await state.set_state(GenerateState.waiting_prompt)

    # turn off loading animation of inline button
    await callback.answer()


# handling any text message if model is selected and start generate with AstriaAPI
@router_generate_image.message(F.text, GenerateState.waiting_prompt)
async def start_generating(message: Message, state: FSMContext):
    # get all data from bot storage
    data = await state.get_data()

    # notify user about starting generation image
    await message.answer(f'⏳ Генерирую изображение с моделью {data["model_id"]}, пожалуйста, подождите...')

    # do request to Astria API, which runs image generation
    astria_api.create_prompt(model_id=data["model_id"],
                             user_id=message.from_user.id,
                             prompt_text=message.text)

