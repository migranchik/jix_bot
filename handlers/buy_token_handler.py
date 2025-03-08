from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import general_keyboards

from states.BuyTokenState import BuyTokenState

# create router for handling buying token
router_buy_token = Router()

# create db adapter objects


# handling the click to buy token (deposit)
@router_buy_token.callback_query(F.data.startswith('buy_token'))
async def start_buy(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Напишите количество токенов, которое хотите пополнить \n\n"
                                     "1 токен = 1 рубль",
                                     reply_markup=general_keyboards.back_to_menu_kb,
                                     parse_mode="HTML")

    await state.set_state(BuyTokenState.waiting_amount)


@router_buy_token.message(BuyTokenState.waiting_amount)
async def create_invoice(message: Message, state: FSMContext):
    await message.answer(message.text + "")

    await state.set_state(None)




