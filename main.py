import logging
logging.basicConfig(level=logging.INFO)

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import settings
from logic.arbitrage import check_arbitrage
from logic.auto_monitor import auto_monitor_loop, get_user_settings

BOT_SYMBOL = 'BTC'

async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    # Запускаем фоновую задачу
    asyncio.create_task(auto_monitor_loop(bot))

    @dp.message(Command('start'))
    async def start(m: Message):
        await m.answer('Bot is running. Use /check, /auto_on, /auto_off')

    @dp.message(Command('check'))
    async def check(m: Message):
        result = await check_arbitrage(BOT_SYMBOL)

        if "error" in result:
            await m.answer(f"⚠️ Ошибка: {result['error']}")
            return

        text = (
            f"📊 *Арбитраж найден:*\n"
            f"🟢 Long на *{result['long']}* @ `{result['long_price']}`\n"
            f"🔴 Short на *{result['short']}* @ `{result['short_price']}`\n"
            f"💰 Потенциальный PnL: *{result['pnl']}$*\n\n"
            f"_Авто‑мониторинг добавим позже_"
        )

        await m.answer(text, parse_mode="Markdown")

    @dp.message(Command('auto_on'))
    async def auto_on(m: Message):
        cfg = get_user_settings(m.from_user.id)
        cfg["enabled"] = True
        await m.answer("🟢 Авто‑мониторинг включён.")

    @dp.message(Command('auto_off'))
    async def auto_off(m: Message):
        cfg = get_user_settings(m.from_user.id)
        cfg["enabled"] = False
        await m.answer("🔴 Авто‑мониторинг выключен.")

    @dp.message(Command('auto_status'))
    async def auto_status(m: Message):
        cfg = get_user_settings(m.from_user.id)
        status = "🟢 Включён" if cfg["enabled"] else "🔴 Выключен"
        await m.answer(
            f"{status}\n"
            f"Монета: {cfg['symbol']}\n"
            f"Интервал: {cfg['interval']} сек\n"
            f"Минимальный PnL: {cfg['min_pnl']}$"
        )

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
