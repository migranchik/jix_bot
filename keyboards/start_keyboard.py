from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# keyboard at the first start of the bot
start_create_model_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Создать модель!', callback_data='start_creating_model')]
    ]
)


# keyboard at the other start of the bot
def get_choose_model_kb(models):
    # list of buttons with user models
    inline_keyboard = []

    for model in models:
        inline_keyboard.append(
            [InlineKeyboardButton(text=model[2], callback_data=f"chose_model_{model[4]}")]
        )
    inline_keyboard.append(
        [InlineKeyboardButton(text='Создать модель!', callback_data='start_creating_model')]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

