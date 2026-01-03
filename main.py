import logging
logging.basicConfig(level=logging.INFO)

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import settings
from logic.arbitrage import check_arbitrage
from logic.auto_monitor import auto_monitor_loop, get_user_settings
from logic.exchange_links import get_exchange_link

from keyboards import (
    main_menu, check_buttons, settings_menu,
    symbol_toggle_menu, interval_menu, min_pnl_menu
)


# === Клавиатура с ссылками на биржи ===
def build_result_keyboard(long_ex, short_ex, symbol):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🟢 {long_ex}",
                    url=get_exchange_link(long_ex, symbol)
                ),
                InlineKeyboardButton(
                    text=f"🔴 {short_ex}",
                    url=get_exchange_link(short_ex, symbol)
                )
            ],
            [
                InlineKeyboardButton(text="🔄 Проверить снова", callback_data="check_again")
            ]
        ]
    )


async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    # Запускаем авто‑мониторинг
    asyncio.create_task(auto_monitor_loop(bot))

    # ============================
    # Команда /start
    # ============================
    @dp.message(Command("start"))
    async def start(m: Message):
        await m.answer("Бот запущен. Выбирай действие:", reply_markup=main_menu)

    # ============================
    # Команда /check
    # ============================
    @dp.message(Command("check"))
    async def check(m: Message):
        cfg = get_user_settings(m.from_user.id)

        for symbol in cfg["symbols"]:
            result = await check_arbitrage(symbol)

            if "error" in result:
                await m.answer(f"⚠️ Ошибка по {symbol}: {result['error']}")
                continue

            text = (
                f"📊 *Арбитраж по {symbol}:*\n"
                f"🟢 Long: *{result['long']}* @ `{result['long_price']}`\n"
                f"🔴 Short: *{result['short']}* @ `{result['short_price']}`\n"
                f"💰 PnL: *{result['pnl']}$*\n"
            )

            kb = build_result_keyboard(result["long"], result["short"], symbol)
            await m.answer(text, parse_mode="Markdown", reply_markup=kb)

    # ============================
    # Команда /settings
    # ============================
    @dp.message(Command("settings"))
    async def settings_cmd(m: Message):
        await m.answer("⚙ Настройки:", reply_markup=settings_menu)

    # ============================
    # CALLBACKS
    # ============================

    # Повторная проверка
    @dp.callback_query(F.data == "check_again")
    async def cb_check_again(c: CallbackQuery):
        cfg = get_user_settings(c.from_user.id)

        for symbol in cfg["symbols"]:
            result = await check_arbitrage(symbol)

            if "error" in result:
                await c.message.answer(f"⚠️ Ошибка по {symbol}: {result['error']}")
                continue

            text = (
                f"📊 *Арбитраж по {symbol}:*\n"
                f"🟢 Long: *{result['long']}* @ `{result['long_price']}`\n"
                f"🔴 Short: *{result['short']}* @ `{result['short_price']}`\n"
                f"💰 PnL: *{result['pnl']}$*\n"
            )

            kb = build_result_keyboard(result["long"], result["short"], symbol)
            await c.message.answer(text, parse_mode="Markdown", reply_markup=kb)

        await c.answer()

    # Авто ON
    @dp.callback_query(F.data == "auto_on")
    async def cb_auto_on(c: CallbackQuery):
        cfg = get_user_settings(c.from_user.id)
        cfg["enabled"] = True
        await c.message.answer("🟢 Авто‑мониторинг включён.")
        await c.answer()

    # Авто OFF
    @dp.callback_query(F.data == "auto_off")
    async def cb_auto_off(c: CallbackQuery):
        cfg = get_user_settings(c.from_user.id)
        cfg["enabled"] = False
        await c.message.answer("🔴 Авто‑мониторинг выключен.")
        await c.answer()

    # Открыть настройки
    @dp.callback_query(F.data == "open_settings")
    async def cb_open_settings(c: CallbackQuery):
        await c.message.answer("⚙ Настройки:", reply_markup=settings_menu)
        await c.answer()

    # === МОНЕТЫ ===
    @dp.callback_query(F.data == "set_symbols")
    async def cb_set_symbols(c: CallbackQuery):
        await c.message.answer("Выбери монеты для мониторинга:", reply_markup=symbol_toggle_menu)
        await c.answer()

    @dp.callback_query(F.data.startswith("toggle_"))
    async def cb_toggle_symbol(c: CallbackQuery):
        symbol = c.data.split("_")[1]
        cfg = get_user_settings(c.from_user.id)

        if symbol in cfg["symbols"]:
            cfg["symbols"].remove(symbol)
            await c.message.answer(f"❌ {symbol} отключён")
        else:
            cfg["symbols"].append(symbol)
            await c.message.answer(f"✅ {symbol} включён")

        await c.answer()

    # === ИНТЕРВАЛ ===
    @dp.callback_query(F.data == "set_interval")
    async def cb_set_interval(c: CallbackQuery):
        await c.message.answer("Выбери интервал:", reply_markup=interval_menu)
        await c.answer()

    @dp.callback_query(F.data.startswith("interval_"))
    async def cb_interval(c: CallbackQuery):
        interval = int(c.data.split("_")[1])
        cfg = get_user_settings(c.from_user.id)
        cfg["interval"] = interval
        await c.message.answer(f"Интервал установлен: {interval} сек")
        await c.answer()

    # === MIN PNL ===
    @dp.callback_query(F.data == "set_min_pnl")
    async def cb_set_min_pnl(c: CallbackQuery):
        await c.message.answer("Выбери минимальный PnL:", reply_markup=min_pnl_menu)
        await c.answer()

    @dp.callback_query(F.data.startswith("pnl_"))
    async def cb_pnl(c: CallbackQuery):
        pnl = int(c.data.split("_")[1])
        cfg = get_user_settings(c.from_user.id)
        cfg["min_pnl"] = pnl
        await c.message.answer(f"Минимальный PnL установлен: {pnl}$")
        await c.answer()

    # Назад в главное меню
    @dp.callback_query(F.data == "back_main")
    async def cb_back_main(c: CallbackQuery):
        await c.message.answer("Главное меню:", reply_markup=main_menu)
        await c.answer()

    # ============================
    # Запуск бота
    # ============================
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
