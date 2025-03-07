from aiogram.fsm.state import StatesGroup, State


# all states are for waiting to receive the details used when creating the model
class CreateModelState(StatesGroup):
    waiting_model_name = State()
    waiting_upload_photos = State()
    confirmation_sent_photos = State()

