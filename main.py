import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import settings

# === ROUTERS ===
from handlers.start import router as start_router
from handlers.check import router as check_router

# === AUTO MONITOR ===
from logic.auto_monitor import auto_monitor_loop

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(check_router)

    # Запускаем авто-мониторинг
    asyncio.create_task(auto_monitor_loop(bot))

    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
