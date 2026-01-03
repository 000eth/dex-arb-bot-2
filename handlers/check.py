from aiogram import types
from logic.exchange_links import get_exchange_link
from logic.auto_monitor import get_user_settings
from logic.arbitrage import check_arbitrage


# Экранирование для MarkdownV2
def esc(text: str) -> str:
    chars = r"\_*[]()~`>#+-=|{}.!"
    for ch in chars:
        text = text.replace(ch, f"\\{ch}")
    return text


@router.message(commands=["check"])
async def handle_check(message: types.Message):
    cfg = get_user_settings(message.from_user.id)

    # Если монеты не заданы — ставим ETH по умолчанию
    symbols = cfg.get("symbols", ["ETH"])

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

        # ссылки
        long_url = get_exchange_link(long_ex, symbol)
        short_url = get_exchange_link(short_ex, symbol)

        # текст с кликабельными биржами
        text = (
            f"📊 *Арбитраж по {esc(symbol)}:*\n"
            f"🟢 Long: [{esc(long_ex)}]({long_url}) @ `{esc(str(long_price))}`\n"
            f"🔴 Short: [{esc(short_ex)}]({short_url}) @ `{esc(str(short_price))}`\n"
            f"💰 PnL: *{esc(str(pnl))}$*\n"
        )

        await message.answer(text, parse_mode="MarkdownV2")
