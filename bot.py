from aiogram import Bot

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

token = config["Bot"]["token"]

bot = Bot(token=token)
