from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.photo_format_dict import photo_formats


def get_choose_photo_format_kb(photo_format_id: int) -> InlineKeyboardMarkup:
    photo_format_num = 0
    inline_keyboard = []

    while photo_format_num < len(photo_formats):
        row_buttons = []
        for i in range(2):
            if photo_format_num == photo_format_id:
                row_buttons.append(
                    InlineKeyboardButton(text=photo_formats[photo_format_num]["text"] + "✅",
                                         callback_data=f"chose_photo_format_{photo_format_num}")
                )
            else:
                row_buttons.append(
                    InlineKeyboardButton(text=photo_formats[photo_format_num]["text"],
                                         callback_data=f"chose_photo_format_{photo_format_num}")
                                   )
            photo_format_num += 1
        inline_keyboard.append(row_buttons)

    inline_keyboard.append([InlineKeyboardButton(text="Выбрал ➡️", callback_data="photo_format_chose")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
