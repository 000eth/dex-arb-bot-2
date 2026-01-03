import logging
logging.basicConfig(level=logging.INFO)

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import settings
from logic.arbitrage import check_arbitrage
from logic.auto_monitor import auto_monitor_loop, get_user_settings
from keyboards import main_menu, check_buttons

BOT_SYMBOL = 'BTC'

async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    asyncio.create_task(auto_monitor_loop(bot))

    @dp.message(Command('start'))
    async def start(m: Message):
        await m.answer(
            "Бот запущен. Выбирай действие:",
            reply_markup=main_menu
        )

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
            f"💰 Потенциальный PnL: *{result['pnl']}$*\n"
        )

        await m.answer(text, parse_mode="Markdown", reply_markup=check_buttons)

    # === INLINE BUTTON HANDLERS ===

    @dp.callback_query(F.data == "check_again")
    async def cb_check_again(c: CallbackQuery):
        result = await check_arbitrage(BOT_SYMBOL)

        if "error" in result:
            await c.message.answer(f"⚠️ Ошибка: {result['error']}")
            return

        text = (
            f"📊 *Арбитраж найден:*\n"
            f"🟢 Long на *{result['long']}* @ `{result['long_price']}`\n"
            f"🔴 Short на *{result['short']}* @ `{result['short_price']}`\n"
            f"💰 PnL: *{result['pnl']}$*\n"
        )

        await c.message.answer(text, parse_mode="Markdown", reply_markup=check_buttons)
        await c.answer()

    @dp.callback_query(F.data == "auto_on")
    async def cb_auto_on(c: CallbackQuery):
        cfg = get_user_settings(c.from_user.id)
        cfg["enabled"] = True
        await c.message.answer("🟢 Авто‑мониторинг включён.")
        await c.answer()

    @dp.callback_query(F.data == "auto_off")
    async def cb_auto_off(c: CallbackQuery):
        cfg = get_user_settings(c.from_user.id)
        cfg["enabled"] = False
        await c.message.answer("🔴 Авто‑мониторинг выключен.")
        await c.answer()

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
