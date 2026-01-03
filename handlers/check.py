# ============================
# Команда /check
# ============================
@dp.message(Command("check"))
async def check(m: Message):
    cfg = get_user_settings(m.from_user.id)

    # Экранируем MarkdownV2
    def esc(text: str) -> str:
        chars = r"\_*[]()~`>#+-=|{}.!"
        for ch in chars:
            text = text.replace(ch, f"\\{ch}")
        return text

    for symbol in cfg["symbols"]:
        result = await check_arbitrage(symbol)

        if "error" in result:
            await m.answer(f"⚠️ Ошибка по {symbol}: {result['error']}")
            continue

        long_ex = result["long"]
        short_ex = result["short"]
        long_price = result["long_price"]
        short_price = result["short_price"]
        pnl = result["pnl"]

        # ссылки
        long_url = get_exchange_link(long_ex, symbol)
        short_url = get_exchange_link(short_ex, symbol)

        # текст с гиперссылками
        text = (
            f"📊 *Арбитраж по {esc(symbol)}:*\n"
            f"🟢 Long: [{esc(long_ex)}]({long_url}) @ `{esc(str(long_price))}`\n"
            f"🔴 Short: [{esc(short_ex)}]({short_url}) @ `{esc(str(short_price))}`\n"
            f"💰 PnL: *{esc(str(pnl))}$*\n"
        )

        await m.answer(text, parse_mode="MarkdownV2")
