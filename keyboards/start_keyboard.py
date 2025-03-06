from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_create_model_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Создать модель!', callback_data='start_creating_model')]
    ]
)
