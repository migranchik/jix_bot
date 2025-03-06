import asyncio
import logging
import uvicorn

from aiogram import Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request

from bot import bot

from handlers import start_handler, create_model_handler
from adapters import model_db_adapter

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаём FastAPI
app = FastAPI()

model_db = model_db_adapter.ModelDB()

# Настраиваем aiogram
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start_handler.router_start)
dp.include_router(create_model_handler.router_create_model)


# Webhook для Astria
@app.post("/astria_callback")
async def astria_callback(request: Request):
    """Обработка коллбэков от Astria"""
    query_params = request.query_params
    user_id = query_params.get('user_id')
    model_title = query_params.get('model_title')

    logging.info(f"Astria callback: user_id={user_id}, model_title={model_title}")

    model_db.update_model_tuned_status(model_title)

    await bot.send_message(user_id, "Model is done")
    return {"status": "received"}


async def start_bot():
    """Запуск бота в режиме polling"""
    await bot.delete_webhook(drop_pending_updates=True)  # Отключаем вебхук у Telegram
    logging.info("✅ Бот запущен в режиме polling")
    await dp.start_polling(bot)


async def start_fastapi():
    """Запуск FastAPI"""
    logging.info("✅ FastAPI запущен на http://0.0.0.0:8000")
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """Запуск FastAPI и бота одновременно"""
    await asyncio.gather(start_bot(), start_fastapi())  # Запускаем оба сервиса


if __name__ == "__main__":
    asyncio.run(main())  # Запуск приложения
