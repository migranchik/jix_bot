from aiogram.fsm.state import StatesGroup, State


# state to wait prompt from user for generating image
class GenerateState(StatesGroup):
    waiting_prompt = State()

