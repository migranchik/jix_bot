from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.types.input_media_photo import InputMediaPhoto

from keyboards import choose_photo_format_keyboard, general_keyboards

from utils.photo_format_dict import photo_formats

# create router for handling choosing photo format
router_choose_photo_format = Router()


# handling the click to choose photo format
@router_choose_photo_format.callback_query(F.data.startswith('choose_photo_format'))
async def choose_photo_format(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    image_url = photo_formats[data["photo_format_id"]]["image_url"]

    # set default image in message
    media = InputMediaPhoto(media=image_url)

    await callback.message.edit_media(
        media=media,
        reply_markup=choose_photo_format_keyboard.get_choose_photo_format_kb(data["photo_format_id"])
    )
    # turn off loading animation of inline button
    await callback.answer()


# handling choice the new photo format
@router_choose_photo_format.callback_query(F.data.startswith('chose_photo_format'))
async def update_photo_format(callback: CallbackQuery, state: FSMContext):
    photo_format_id = int(callback.data.split('_')[3])
    print(photo_format_id)

    await state.update_data(photo_format_id=photo_format_id)

    image_url = photo_formats[photo_format_id]["image_url"]

    # change image in message
    media = InputMediaPhoto(media=image_url)

    await callback.message.edit_media(
        media=media,
        reply_markup=choose_photo_format_keyboard.get_choose_photo_format_kb(photo_format_id),
    )

    # turn off loading animation of inline button
    await callback.answer()


@router_choose_photo_format.callback_query(F.data.startswith('photo_format_chose'))
async def photo_format_chose(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photo_format_id = data["photo_format_id"]

    await callback.message.answer(f"✅ Установлен формат фото - {photo_formats[photo_format_id]['text']} \n"
                                  f"Давай скорее творить!❤️",
                                  reply_markup=general_keyboards.back_to_menu_kb,
                                  parse_mode="HTML")
    await callback.message.delete()

