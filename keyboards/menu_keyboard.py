from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# menu inline keyboard
menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать фотосессию", callback_data="start_generate")],
        [InlineKeyboardButton(text="Личный кабинет", callback_data="profile")],
        [InlineKeyboardButton(text="Выбрать формат фото", callback_data="choose_photo_format")],
        [InlineKeyboardButton(text="Мои модели", callback_data="my_models")],
        [InlineKeyboardButton(text="Пополнить баланс", callback_data="buy_token")]
    ]
)
