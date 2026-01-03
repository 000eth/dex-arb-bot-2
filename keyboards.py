from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# === ГЛАВНОЕ МЕНЮ (кнопки без слешей) ===
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Check")],
        [KeyboardButton(text="Settings")]
    ],
    resize_keyboard=True
)


# === МЕНЮ НАСТРОЕК ===
settings_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Монеты", callback_data="set_symbols")],
    [InlineKeyboardButton(text="Интервал", callback_data="set_interval")],
    [InlineKeyboardButton(text="Минимальный PnL", callback_data="set_min_pnl")],
    [InlineKeyboardButton(text="Авто‑мониторинг", callback_data="toggle_auto")],
])


# === ДИНАМИЧЕСКОЕ МЕНЮ ВЫБОРА МОНЕТ (✔/✖) ===
def build_symbol_menu(selected: list[str]) -> InlineKeyboardMarkup:
    def btn(symbol: str):
        mark = "✔" if symbol in selected else "✖"
        return InlineKeyboardButton(
            text=f"{symbol} {mark}",
            callback_data=f"toggle_{symbol}"
        )

    keyboard = [
        [btn("BTC"), btn("ETH")],
        [btn("SOL"), InlineKeyboardButton(text="Назад", callback_data="back_settings")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# === МЕНЮ ИНТЕРВАЛОВ ===
interval_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="5 сек", callback_data="interval_5"),
        InlineKeyboardButton(text="10 сек", callback_data="interval_10"),
    ],
    [
        InlineKeyboardButton(text="30 сек", callback_data="interval_30"),
        InlineKeyboardButton(text="Назад", callback_data="back_settings")
    ]
])


# === МЕНЮ МИНИМАЛЬНОГО PnL ===
min_pnl_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="1$", callback_data="pnl_1"),
        InlineKeyboardButton(text="5$", callback_data="pnl_5"),
    ],
    [
        InlineKeyboardButton(text="10$", callback_data="pnl_10"),
        InlineKeyboardButton(text="Назад", callback_data="back_settings")
    ]
])
