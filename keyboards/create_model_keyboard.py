from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# keyboard to choose sex for new model
choose_gender_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👨‍🦰 Мужчина", callback_data="chose_man_Мужчина")],
        [InlineKeyboardButton(text="👱‍♀️ Женщина", callback_data="chose_woman_Женщина")]
    ]
)

# button to start learning new model
start_model_learning_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать обучение!", callback_data="start_learning")]
    ]
)