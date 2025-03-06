from aiogram.fsm.state import StatesGroup, State


# all states for creating model
class CreateModelState(StatesGroup):
    waiting_model_name = State()
    waiting_upload_photos = State()
    confirmation_sent_photos = State()

