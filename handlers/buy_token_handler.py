import configparser

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards import general_keyboards, buy_token_keyboard

from adapters import user_db_adapter

from states.BuyTokenState import BuyTokenState

from yookassa import Configuration, Payment
from utils import create_yookassa_payload

config = configparser.ConfigParser()
config.read('config.ini')

card_shop_id = config["Yookassa"]["cardshopid"]
token = config["Yookassa"]["token"]

#Configuration.account_id = card_shop_id
#Configuration.secret_key = token

# create router for handling buying token
router_buy_token = Router()

# create db adapter objects
user_db = user_db_adapter.UserDB()


# handling the click to buy token (deposit)
@router_buy_token.callback_query(F.data.startswith('buy_token'))
async def start_buy(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Напишите количество токенов, которое хотите пополнить \n\n"
                                     "1 токен = 1 рубль",
                                     reply_markup=general_keyboards.back_to_menu_kb,
                                     parse_mode="HTML")

    await state.set_state(BuyTokenState.waiting_amount)


@router_buy_token.message(Command('buy_tokens'))
async def start_buy(message: Message, state: FSMContext):
    await message.answer("Напишите количество токенов, которое хотите пополнить \n\n"
                         "1 токен = 1 рубль",
                         reply_markup=general_keyboards.back_to_menu_kb,
                         parse_mode="HTML")

    await message.delete()
    await state.set_state(BuyTokenState.waiting_amount)


@router_buy_token.message(BuyTokenState.waiting_amount)
async def create_invoice(message: Message, state: FSMContext):
    try:
        token_amount = int(message.text)
        await state.update_data(token_amount=token_amount)
        """
        payment = create_yookassa_payload.create_yookassa_payload(token_amount, "Пополнение баланса")

        await message.answer(f'Пополняемое количество токенов: {token_amount}\n\n'
                             f'Никто кроме банка и интернет-эквайринга не имеет доступа к вашим банковским данным',
                             reply_markup=buy_token_keyboard.get_pay_kb(payment.confirmation["confirmation_url"],
                                                                        payment.id)
                            )
        """

        await message.answer(f'Пополняемое количество токенов: {token_amount}\n\n'
                             f'Никто кроме банка и интернет-эквайринга не имеет доступа к вашим банковским данным',
                             reply_markup=buy_token_keyboard.get_pay_kb("https://google.com",
                                                                        123)
                             )

        await state.set_state(None)
    except Exception as e:
        print("Error", e)
        await message.answer("Введите одно число - количество токенов, которое хотитет пополнить")


@router_buy_token.callback_query(F.data.startswith('check_payment'))
async def check_pay(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.answer()

    payment_id = callback.data.split('_')[2]
    #payment = Payment.find_one(payment_id)
    paid = True #payment.paid

    if paid:
        user_tokens = user_db.get_user_tokens(callback.from_user.id)
        new_amount = user_tokens + data["token_amount"]

        user_db.up_user_tokens(user_id=callback.from_user.id,
                               new_amount=new_amount)

        await callback.message.answer(
            f'Ваш баланс успешно пополнен. Сумма пополнения: {data["token_amount"]}\n'
            f'Пора возвращаться назад в меню\n\n',
            reply_markup=general_keyboards.back_to_menu_kb,
            parse_mode="HTML")

        await callback.message.delete()
    else:
        await callback.answer('Вы не оплатили!', show_alert=True)



