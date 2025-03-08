from aiogram.fsm.state import StatesGroup, State


# state to wait prompt from user for generating image
class BuyTokenState(StatesGroup):
    waiting_amount = State()

