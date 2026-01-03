import logging
logging.basicConfig(level=logging.INFO)

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import settings


async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start(m: Message):
        await m.answer("Бот жив. Это минимальный тестовый ответ.")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
