from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню настроек
settings_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Монеты", callback_data="set_symbols")],
    [InlineKeyboardButton(text="Интервал", callback_data="set_interval")],
    [InlineKeyboardButton(text="Минимальный PnL", callback_data="set_min_pnl")],
])

# Меню выбора монет
symbol_toggle_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="BTC", callback_data="toggle_BTC"),
        InlineKeyboardButton(text="ETH", callback_data="toggle_ETH"),
    ],
    [
        InlineKeyboardButton(text="SOL", callback_data="toggle_SOL"),
        InlineKeyboardButton(text="Назад", callback_data="back_settings")
    ]
])

# Меню интервалов
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

# Меню минимального PnL
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
