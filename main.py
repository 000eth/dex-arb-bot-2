import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import settings

from handlers.start import router as start_router
from handlers.settings import router as settings_router
from handlers.check import router as check_router

from logic.auto_monitor import auto_monitor_loop

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(settings_router)
    dp.include_router(check_router)

    asyncio.create_task(auto_monitor_loop(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
