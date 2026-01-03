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

    # ссылки
    long_url = get_exchange_link(long_ex, "ETH")
    short_url = get_exchange_link(short_ex, "ETH")

    # Экранируем MarkdownV2
    def esc(t: str) -> str:
        return t.replace("-", "\\-").replace(".", "\\.").replace("_", "\\_")

    text = (
        f"📊 *Арбитраж по ETH:*\n"
        f"🟢 Long: [{esc(long_ex)}]({long_url}) @ `{long_price}`\n"
        f"🔴 Short: [{esc(short_ex)}]({short_url}) @ `{short_price}`\n"
        f"💰 PnL: *{pnl}$*\n"
    )

    await message.answer(text, parse_mode="MarkdownV2")
