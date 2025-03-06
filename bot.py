from aiogram import Bot
from models.astria_api import AstriaApi

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

token = config["Bot"]["token"]
api_key = config["Astria"]["api_key"]

bot = Bot(token=token)
astria_api = AstriaApi(api_key, callback_url="https://4c1a-2a01-e5c0-3a6a-00-2.ngrok-free.app/astria_callback")

