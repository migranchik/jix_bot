from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import style_list_pagination_keyboard

from utils.image_styles import styles


# create router for handling generate image
router_style_list_pagination = Router()

# create db adapter objects


# handling the click to start photo session
@router_style_list_pagination.callback_query(F.data.startswith('start_generate'))
async def choose_style(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    style_list_num = 1
    await state.update_data(style_list_num=style_list_num)

    styles_count = len(styles)
    list_count = styles_count // 3
    if styles_count % 3 != 0:
        list_count += 1

    first_style_in_page = (style_list_num - 1) * 3
    last_style_in_page = style_list_num * 3

    await callback.message.edit_text("Выберите стиль для фотографий",
                                     reply_markup=style_list_pagination_keyboard.get_styles_swiper(list_num=style_list_num,
                                                                                            list_count=list_count,
                                                                                            styles=styles[first_style_in_page:last_style_in_page]))


@router_style_list_pagination.callback_query(F.data.startswith('next_event'))
async def next_list(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    style_list_num = data['style_list_num'] + 1

    await state.update_data(style_list_num=style_list_num)

    styles_count = len(styles)
    list_count = styles_count // 3
    if styles_count % 3 != 0:
        list_count += 1

    first_style_in_page = (style_list_num - 1) * 3
    last_style_in_page = style_list_num * 3

    await callback.message.edit_text("Выберите стиль для фотографий",
                                  reply_markup=style_list_pagination_keyboard.get_styles_swiper(list_num=style_list_num,
                                                                                         list_count=list_count,
                                                                                         styles=styles[
                                                                                                first_style_in_page:last_style_in_page]))


@router_style_list_pagination.callback_query(F.data.startswith('prev_event'))
async def prev_list(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    style_list_num = data['style_list_num'] - 1

    await state.update_data(style_list_num=style_list_num)

    styles_count = len(styles)
    list_count = styles_count // 3
    if styles_count % 3 != 0:
        list_count += 1

    first_style_in_page = (style_list_num - 1) * 3
    last_style_in_page = style_list_num * 3

    await callback.message.edit_text("Выберите стиль для фотографий",
                                     reply_markup=style_list_pagination_keyboard.get_styles_swiper(list_num=style_list_num,
                                                                                            list_count=list_count,
                                                                                            styles=styles[
                                                                                                   first_style_in_page:last_style_in_page]))




