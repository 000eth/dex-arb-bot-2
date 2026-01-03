from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.exchange_links import get_exchange_link


@router.message(commands=["check"])
async def handle_check(message: types.Message):
    result = await check_arbitrage("ETH")

    if "error" in result:
        await message.answer("⚠️ Не удалось получить данные с бирж.")
        return

    long_ex = result["long"]
    short_ex = result["short"]
    long_price = result["long_price"]
    short_price = result["short_price"]
    pnl = result["pnl"]

    text = (
        f"📊 *Арбитраж по ETH:*\n"
        f"🟢 Long: *{long_ex}* @ `{long_price}`\n"
        f"🔴 Short: *{short_ex}* @ `{short_price}`\n"
        f"💰 PnL: *{pnl}$*\n"
    )

    # === Кнопки со ссылками ===
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🟢 {long_ex}",
                    url=get_exchange_link(long_ex, "ETH")
                ),
                InlineKeyboardButton(
                    text=f"🔴 {short_ex}",
                    url=get_exchange_link(short_ex, "ETH")
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
