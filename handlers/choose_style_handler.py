from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.utils.media_group import MediaGroupBuilder

from keyboards import style_list_pagination_keyboard

from utils.image_styles import styles


# create router for handling generate image
router_choose_style = Router()

# create db adapter objects


# handling the click to start photo session
@router_choose_style.callback_query(F.data.startswith('chose_style'))
async def choose_style(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    style_id = int(callback.data.split('_')[2])

    album_builder = MediaGroupBuilder(
        caption="Выберите понравившийся вам пример"
    )

    images = styles[style_id]["images"]
    for image in images:
        album_builder.add_photo(media=image)

    await callback.message.answer_media_group(media=album_builder.build())
