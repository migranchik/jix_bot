import asyncio
import logging
import uvicorn
import json

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request

from bot import bot

from handlers import (start_handler,
                      create_model_handler,
                      choose_model_handler,
                      menu_handler,
                      profile_handler,
                      my_models_handler,
                      buy_token_handler,
                      choose_style_handler,
                      choose_photo_format_handler,
                      style_list_pagination_handler)

from adapters import model_db_adapter

# logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI
app = FastAPI()

# Adapter for models table in DB
model_db = model_db_adapter.ModelDB()

# setting up aiogram
dp = Dispatcher(storage=MemoryStorage())

# include routers from handler files
dp.include_router(menu_handler.router_menu)
dp.include_router(start_handler.router_start)
dp.include_router(create_model_handler.router_create_model)
dp.include_router(choose_model_handler.router_choose_model)
dp.include_router(profile_handler.router_profile)
dp.include_router(my_models_handler.router_my_models)
dp.include_router(buy_token_handler.router_buy_token)
dp.include_router(choose_photo_format_handler.router_choose_photo_format)
dp.include_router(style_list_pagination_handler.router_style_list_pagination)
dp.include_router(choose_style_handler.router_choose_style)


# webhook endpoint for fine-tuning model from Astria
@app.post("/model")
async def astria_callback(request: Request):
    # get query params from callback url
    query_params = request.query_params
    user_id = query_params.get('user_id')
    model_title = query_params.get('model_title')

    logging.info(f"Astria callback: user_id={user_id}, model_title={model_title}")

    # change model status `tuned` in models table
    model_db.update_model_tuned_status(model_title)

    # notify user about readiness of his model
    await bot.send_message(user_id, "Ваша модель готова к работе! Напишите /start и выберите её")
    return {"status": "received"}


# webhook endpoint for prompt from Astria
@app.post("/prompt")
async def astria_callback(request: Request):
    # get query params from callback url
    query_params = request.query_params
    user_id = query_params.get('user_id')
    model_id = query_params.get('model_id')

    logging.info(f"Astria callback: user_id={user_id}, model_id={model_id}")

    # get Prompt object from callback
    body = await request.body()

    # Decode body in bytes to string body
    json_str = body.decode("utf-8")
    json_obj = json.loads(json_str)

    # take the generated image url from callback body
    image_url = json_obj["prompt"]["images"][0]

    # notify user about readiness his image
    await bot.send_photo(user_id, photo=image_url, caption='Вот ваша картинка')

    return {"status": "received"}


async def start_bot():
    # function start bot in polling mode
    await bot.delete_webhook(drop_pending_updates=True)  # turn off webhook from Telegram
    logging.info("✅ Бот запущен в режиме polling")
    await dp.start_polling(bot)


async def start_fastapi():
    # function start FastAPI for handle callbacks from Astria API
    logging.info("✅ FastAPI запущен на http://0.0.0.0:8000")
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    # start bot and FastAPI
    await asyncio.gather(start_bot(), start_fastapi())  # start both


if __name__ == "__main__":
    asyncio.run(main())  # run application
