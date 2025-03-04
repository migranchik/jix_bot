import asyncio
import logging

from bot import bot

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import (start_handler)

# логгирование в файл
# logging.basicConfig(
#      filename='bot.log',  # Укажите путь к файлу логов
#      level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )

# логгирование для тестирования
logging.basicConfig(level=logging.INFO)


# Запуск бота
async def main():
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_handler.router_start)


    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
