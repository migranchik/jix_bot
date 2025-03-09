from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_styles_swiper(list_num: int, list_count: int, styles: list) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for style in styles:
        inline_keyboard.append([InlineKeyboardButton(text=style["name"],
                                                    callback_data=f"chose_style_{style['id']}")])

    next_list_button = InlineKeyboardButton(text='->', callback_data=f'next_event')
    prev_list_button = InlineKeyboardButton(text='<-', callback_data=f'prev_event')
    list_num_button = InlineKeyboardButton(text=f'{list_num}/{list_count}', callback_data='#')

    if list_num == 1:
        inline_keyboard.append([list_num_button, next_list_button])
    elif list_num == list_count:
        inline_keyboard.append([prev_list_button, list_num_button])
    else:
        inline_keyboard.append([prev_list_button, list_num_button, next_list_button])

    inline_keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
