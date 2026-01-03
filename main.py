import logging
logging.basicConfig(level=logging.INFO)

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import settings
from logic.arbitrage import check_arbitrage  # наш новый арбитраж

BOT_SYMBOL = 'ETH'  # можно сменить на SOL, если хочешь


async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(Command('start'))
    async def start(m: Message):
        await m.answer('Bot is running. Use /check')

    @dp.message(Command('check'))
    async def check(m: Message):
        result = await check_arbitrage(BOT_SYMBOL)

        if "error" in result:
            await m.answer("⚠️ Не удалось получить данные с бирж.")
            return

        long_ex = result["long"]
        short_ex = result["short"]
        long_price = result["long_price"]
        short_price = result["short_price"]
        pnl = result["pnl"]

        text = (
            f"📊 *Арбитраж найден:*\n"
            f"🟢 Long на *{long_ex}* @ `{long_price}`\n"
            f"🔴 Short на *{short_ex}* @ `{short_price}`\n"
            f"💰 Потенциальный PnL: *{pnl}$*\n\n"
            f"_Авто‑мониторинг добавим позже_"
        )

        await m.answer(text, parse_mode="Markdown")

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
