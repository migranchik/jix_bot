from aiogram import Bot
from models.astria_api import AstriaApi

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# take configs from file `config.ini`
token = config["Bot"]["token"]
api_key = config["Astria"]["api_key"]

# create Bot object
bot = Bot(token=token)

# create AstriaAPI model to work with Astria API
astria_api = AstriaApi(api_key, callback_url="https://6bb2-2a01-e5c0-3a6a-00-2.ngrok-free.app/astria_callback/")

