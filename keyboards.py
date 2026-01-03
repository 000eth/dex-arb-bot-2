from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

# ============================
# Главное меню
# ============================

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/check")],
        [KeyboardButton(text="/auto_on"), KeyboardButton(text="/auto_off")],
        [KeyboardButton(text="/settings")],
    ],
    resize_keyboard=True
)

# ============================
# Кнопки под сообщением /check
# ============================

check_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Проверить снова", callback_data="check_again")],
        [
            InlineKeyboardButton(text="▶️ Авто ON", callback_data="auto_on"),
            InlineKeyboardButton(text="⏹ Авто OFF", callback_data="auto_off")
        ],
        [InlineKeyboardButton(text="⚙ Настройки", callback_data="open_settings")]
    ]
)

# ============================
# Меню настроек
# ============================

settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Монеты", callback_data="set_symbols")],
        [InlineKeyboardButton(text="Интервал", callback_data="set_interval")],
        [InlineKeyboardButton(text="Минимальный PnL", callback_data="set_min_pnl")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back_main")]
    ]
)

# ============================
# Меню выбора монет (вкл/выкл)
# ============================

symbol_toggle_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="BTC", callback_data="toggle_BTC"),
            InlineKeyboardButton(text="ETH", callback_data="toggle_ETH"),
            InlineKeyboardButton(text="SOL", callback_data="toggle_SOL"),
        ],
        [
            InlineKeyboardButton(text="⬅ Назад", callback_data="open_settings")
        ]
    ]
)

# ============================
# Меню выбора интервала
# ============================

interval_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1 сек", callback_data="interval_1")],
        [InlineKeyboardButton(text="3 сек", callback_data="interval_3")],
        [InlineKeyboardButton(text="5 сек", callback_data="interval_5")],
        [InlineKeyboardButton(text="10 сек", callback_data="interval_10")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="open_settings")]
    ]
)

# ============================
# Меню выбора минимального PnL
# ============================

min_pnl_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1$", callback_data="pnl_1")],
        [InlineKeyboardButton(text="3$", callback_data="pnl_3")],
        [InlineKeyboardButton(text="5$", callback_data="pnl_5")],
        [InlineKeyboardButton(text="10$", callback_data="pnl_10")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="open_settings")]
    ]
)
