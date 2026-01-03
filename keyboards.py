from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Главное меню (обычные кнопки)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/check")],
        [KeyboardButton(text="/auto_on"), KeyboardButton(text="/auto_off")],
        [KeyboardButton(text="/auto_status")],
    ],
    resize_keyboard=True
)

# Кнопки под сообщением (inline)
check_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Проверить снова", callback_data="check_again")
        ],
        [
            InlineKeyboardButton(text="▶️ Включить авто", callback_data="auto_on"),
            InlineKeyboardButton(text="⏹ Выключить авто", callback_data="auto_off")
        ]
    ]
)
