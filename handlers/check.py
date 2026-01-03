from aiogram import Router, types, F
from aiogram.filters import Command

from logic.arbitrage import check_arbitrage
from logic.exchange_links import get_exchange_link
from logic.auto_monitor import get_user_settings

router = Router()


# Экранируем MarkdownV2
def esc(text: str) -> str:
    chars = r"\_*[]()~`>#+-=|{}.!"
    for ch in chars:
        text = text.replace(ch, f"\\{ch}")
    return text


# Обрабатываем и /check, и кнопку "Check"
@router.message(Command("check"))
@router.message(F.text == "Check")
async def handle_check(message: types.Message):
    cfg = get_user_settings(message.from_user.id)
    symbols = cfg.get("symbols", ["BTC"])

    for symbol in symbols:
        result = await check_arbitrage(symbol)

        if "error" in result:
            await message.answer(f"⚠️ Ошибка по {symbol}: {result['error']}")
            continue

        long_ex = result["long"]
        short_ex = result["short"]
        long_price = result["long_price"]
        short_price = result["short_price"]
        pnl = result["pnl"]

        long_url = get_exchange_link(long_ex, symbol)
        short_url = get_exchange_link(short_ex, symbol)

        text = (
            f"📊 *Арбитраж по {esc(symbol)}:*\n"
            f"🟢 Long: [{esc(long_ex)}]({long_url}) @ `{esc(str(long_price))}`\n"
            f"🔴 Short: [{esc(short_ex)}]({short_url}) @ `{esc(str(short_price))}`\n"
            f"💰 PnL: *{esc(str(pnl))}$*\n"
        )

        await message.answer(
            text,
            parse_mode="MarkdownV2",
            disable_web_page_preview=True
        )
