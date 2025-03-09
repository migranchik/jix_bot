from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_pay_kb(pay_url: str, payment_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить', url=pay_url)],
        [InlineKeyboardButton(text='🔄 Проверить пополнение', callback_data=f'check_payment_{payment_id}')],
        [InlineKeyboardButton(text='⬅️ Назад', callback_data='menu')]
    ])
