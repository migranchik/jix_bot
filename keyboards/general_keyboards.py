from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# menu inline keyboard
back_to_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="menu")],
    ]
)
