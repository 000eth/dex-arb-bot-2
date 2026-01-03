from aiogram import Router, types, F
from keyboards import (
    settings_menu,
    interval_menu,
    min_pnl_menu,
    build_symbol_menu
)
from logic.auto_monitor import get_user_settings

router = Router()


# === Главное меню настроек ===
@router.message(F.text == "Settings")
async def settings_cmd(message: types.Message):
    await message.answer(
        "⚙ Настройки:",
        reply_markup=settings_menu
    )


# === Меню выбора монет ===
@router.callback_query(F.data == "set_symbols")
async def cb_set_symbols(callback: types.CallbackQuery):
    cfg = get_user_settings(callback.from_user.id)
    menu = build_symbol_menu(cfg["symbols"])

    await callback.message.edit_text(
        "Выбери монеты для мониторинга:",
        reply_markup=menu
    )
    await callback.answer()


# === Переключение монеты ===
@router.callback_query(F.data.startswith("toggle_"))
async def cb_toggle_symbol(callback: types.CallbackQuery):
    symbol = callback.data.split("_")[1]
    cfg = get_user_settings(callback.from_user.id)

    # Переключаем монету
    if symbol in cfg["symbols"]:
        cfg["symbols"].remove(symbol)
    else:
        cfg["symbols"].append(symbol)

    # Обновляем меню
    menu = build_symbol_menu(cfg["symbols"])

    await callback.message.edit_text(
        "Выбери монеты для мониторинга:",
        reply_markup=menu
    )
    await callback.answer(f"{symbol} переключён")


# === Меню интервала ===
@router.callback_query(F.data == "set_interval")
async def cb_set_interval(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выбери интервал:",
        reply_markup=interval_menu
    )
    await callback.answer()


# === Установка интервала ===
@router.callback_query(F.data.startswith("interval_"))
async def cb_interval(callback: types.CallbackQuery):
    interval = int(callback.data.split("_")[1])
    cfg = get_user_settings(callback.from_user.id)
    cfg["interval"] = interval

    await callback.message.edit_text(
        f"Интервал установлен: {interval} сек",
        reply_markup=settings_menu
    )
    await callback.answer()


# === Меню минимального PnL ===
@router.callback_query(F.data == "set_min_pnl")
async def cb_set_min_pnl(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выбери минимальный PnL:",
        reply_markup=min_pnl_menu
    )
    await callback.answer()


# === Установка минимального PnL ===
@router.callback_query(F.data.startswith("pnl_"))
async def cb_pnl(callback: types.CallbackQuery):
    pnl = int(callback.data.split("_")[1])
    cfg = get_user_settings(callback.from_user.id)
    cfg["min_pnl"] = pnl

    await callback.message.edit_text(
        f"Минимальный PnL установлен: {pnl}$",
        reply_markup=settings_menu
    )
    await callback.answer()


# === Включение / выключение авто‑мониторинга ===
@router.callback_query(F.data == "toggle_auto")
async def cb_toggle_auto(callback: types.CallbackQuery):
    cfg = get_user_settings(callback.from_user.id)

    cfg["enabled"] = not cfg["enabled"]
    status = "Включён" if cfg["enabled"] else "Выключен"

    await callback.message.edit_text(
        f"⚙ Настройки:\nАвто‑мониторинг: *{status}*",
        reply_markup=settings_menu,
        parse_mode="Markdown"
    )
    await callback.answer(f"Авто‑мониторинг: {status}")


# === Кнопка "Назад" ===
@router.callback_query(F.data == "back_settings")
async def cb_back(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "⚙ Настройки:",
        reply_markup=settings_menu
    )
    await callback.answer()
