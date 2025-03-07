from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType

from bot import bot
from bot import astria_api

from adapters import model_db_adapter, learn_photo_db_adapter
from keyboards import create_model_keyboard
from states.CreateModelState import CreateModelState
from middlewares.AlbumMiddleware import AlbumMiddleware

import uuid

# create router for handling create model
router_create_model = Router()

# include AlbumMiddleware to create model router
router_create_model.message.middleware(AlbumMiddleware())

# create db adapter objects
model_db = model_db_adapter.ModelDB()
learn_photo_db = learn_photo_db_adapter.LearnPhotoDB()


# handling the click to inline button "Создать модель"
@router_create_model.callback_query(F.data.startswith('start_creating_model'))
async def start_model_creating(callback: CallbackQuery, state: FSMContext):
    # set waiting model name state
    await state.set_state(CreateModelState.waiting_model_name)

    # ask model name
    await callback.message.answer("Введи название своей модели одним английским словом \n\n"
                                  "Примеры: annaSokolova, Anna_Sokolova")

    # turn off loading animation of inline button
    await callback.answer()


# get model name from user
@router_create_model.message(CreateModelState.waiting_model_name)
async def get_model_name(message: Message, state: FSMContext):
    # save model name in bot storage
    await state.update_data(model_name=message.text)

    # suggest choosing a gender
    await message.answer("Выберите пол (для улучшения генерации фотографий)",
                         reply_markup=create_model_keyboard.choose_gender_kb)


# handling selected `man` gender
@router_create_model.callback_query(F.data.startswith('chose_man'))
async def chose_man(callback: CallbackQuery, state: FSMContext):
    # get gender from inline button callback data
    gender = callback.data.split('_')[2]

    # set waiting upload photos state
    await state.set_state(CreateModelState.waiting_upload_photos)
    # save user gender in bot storage
    await state.update_data(gender="man")

    # message about selected gender
    await callback.message.answer(f'Вы выбрали пол: <b>{gender}</b>.',
                                  parse_mode="HTML")
    # ask upload photos
    await callback.message.answer('Выбери и загрузи 10-15 своих фотографий ( тут надо будет инструкцию )')

    # turn off loading animation of inline button
    await callback.answer()


# handling selected `woman` gender
@router_create_model.callback_query(F.data.startswith('chose_woman'))
async def chose_woman(callback: CallbackQuery, state: FSMContext):
    # get gender from inline button callback data
    gender = callback.data.split('_')[2]

    # set waiting upload photos state
    await state.set_state(CreateModelState.waiting_upload_photos)
    # save user gender in bot storage
    await state.update_data(gender="woman")

    # message about selected gender
    await callback.message.answer(f'Вы выбрали пол: <b>{gender}</b>.',
                                  parse_mode="HTML")
    # ask upload photos
    await callback.message.answer('Выбери и загрузи 5-10 своих фотографий ( тут надо будет инструкцию )')

    # turn off loading animation of inline button
    await callback.answer()


@router_create_model.message(CreateModelState.waiting_upload_photos)
async def get_user_photos(message: Message, state: FSMContext, album: list[Message] = None):
    model_title = str(uuid.uuid4())

    await state.update_data(model_title=model_title)

    if album:
        try:
            for num, msg in enumerate(album, start=0):
                await bot.download(msg.photo[-1].file_id, f"{message.from_user.id}_{num}.jpg"),

                learn_photo_db.add_photo(file_id=msg.photo[-1].file_id,
                                         file_name=f"{message.from_user.id}_{num}.jpg",
                                         user_id=message.from_user.id,
                                         model_title=model_title)

            await message.answer(f"Загружено фотографий: {len(album)}, нажмите кнопку, чтобы начать обучение",
                                 reply_markup=create_model_keyboard.start_model_learning_kb)

            await state.update_data(count_photo=len(album))
            await state.set_state(None)

        except Exception as e:
            print('Error', e)
            await message.answer("Произошла ошибка")

    else:
        await message.answer('Кажется вы отправили не фотографии или их слишком мало, отправьте от 2 до 10 фотографий')


@router_create_model.callback_query(F.data.startswith('start_learning'))
async def start_model_learning(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    image_names = learn_photo_db.get_user_photo_file_names(data["model_title"])
    images = []

    for image in image_names:
        images.append(('tune[images][]', open(image, 'rb')))

    response = astria_api.create_model(user_id=callback.from_user.id,
                                       gender=data["gender"],
                                       model_title=data["model_title"],
                                       images=images)
    model_data = response.json()

    model_db.create_model(user_id=callback.from_user.id,
                          model_name=data["model_name"],
                          model_id=model_data["id"],
                          model_title=model_data["title"])

    await callback.message.answer("Модель обучается, это займет некоторые время. Мы сообщим вам, когда будет готова к работе")

    # turn off loading animation of inline button
    await callback.answer()
