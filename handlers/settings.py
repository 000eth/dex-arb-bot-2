from aiogram import Router, types
from aiogram.filters import Command

from keyboards import settings_menu, symbol_toggle_menu, interval_menu, min_pnl_menu
from logic.auto_monitor import get_user_settings

router = Router()


@router.message(Command("settings"))
async def settings_cmd(message: types.Message):
    await message.answer("⚙ Настройки:", reply_markup=settings_menu)


# === CALLBACKS ===

@router.callback_query(lambda c: c.data == "set_symbols")
async def cb_set_symbols(c: types.CallbackQuery):
    await c.message.answer("Выбери монеты для мониторинга:", reply_markup=symbol_toggle_menu)
    await c.answer()


@router.callback_query(lambda c: c.data.startswith("toggle_"))
async def cb_toggle_symbol(c: types.CallbackQuery):
    symbol = c.data.split("_")[1]
    cfg = get_user_settings(c.from_user.id)

    if symbol in cfg["symbols"]:
        cfg["symbols"].remove(symbol)
        await c.message.answer(f"❌ {symbol} отключён")
    else:
        cfg["symbols"].append(symbol)
        await c.message.answer(f"✅ {symbol} включён")

    await c.answer()


@router.callback_query(lambda c: c.data == "set_interval")
async def cb_set_interval(c: types.CallbackQuery):
    await c.message.answer("Выбери интервал:", reply_markup=interval_menu)
    await c.answer()


@router.callback_query(lambda c: c.data.startswith("interval_"))
async def cb_interval(c: types.CallbackQuery):
    interval = int(c.data.split("_")[1])
    cfg = get_user_settings(c.from_user.id)
    cfg["interval"] = interval
    await c.message.answer(f"Интервал установлен: {interval} сек")
    await c.answer()


@router.callback_query(lambda c: c.data == "set_min_pnl")
async def cb_set_min_pnl(c: types.CallbackQuery):
    await c.message.answer("Выбери минимальный PnL:", reply_markup=min_pnl_menu)
    await c.answer()


@router.callback_query(lambda c: c.data.startswith("pnl_"))
async def cb_pnl(c: types.CallbackQuery):
    pnl = int(c.data.split("_")[1])
    cfg = get_user_settings(c.from_user.id)
    cfg["min_pnl"] = pnl
    await c.message.answer(f"Минимальный PnL установлен: {pnl}$")
    await c.answer()
