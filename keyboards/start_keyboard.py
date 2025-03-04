from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

continue_to_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продолжить ➡️', callback_data='continue_to_register')]
    ]
)
