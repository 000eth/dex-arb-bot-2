from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.exchange_links import get_exchange_link
from logic.auto_monitor import get_user_settings


@router.message(commands=["check"])
async def handle_check(message: types.Message):
    cfg = get_user_settings(message.from_user.id)

    # Если монеты не заданы — ставим BTC по умолчанию
    symbols = cfg.get("symbols", ["BTC"])

    for symbol in symbols:
        result = await check_arbitrage(symbol)

        if "error" in result:
            await message.answer(f"⚠️ Не удалось получить данные по {symbol}.")
            continue

        long_ex = result["long"]
        short_ex = result["short"]
        long_price = result["long_price"]
        short_price = result["short_price"]
        pnl = result["pnl"]

        text = (
            f"📊 *Арбитраж по {symbol}:*\n"
            f"🟢 Long: *{long_ex}* @ `{long_price}`\n"
            f"🔴 Short: *{short_ex}* @ `{short_price}`\n"
            f"💰 PnL: *{pnl}$*\n"
        )

        # === Кнопки со ссылками на биржи ===
        kb = InlineKeyboardMarkup(
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
                    InlineKeyboardButton(
                        text="🔄 Проверить снова",
                        callback_data="check_again"
                    )
                ]
            ]
        )

        await message.answer(text, parse_mode="Markdown", reply_markup=kb)
