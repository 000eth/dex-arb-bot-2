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

    print("=== HANDLE_CHECK FROM HANDLERS/CHECK.PY ===")

    text = (
        f"🔍 ТЕСТОВЫЙ ВЫВОД — ЭТО НОВЫЙ КОД"
        f"📈 Long на *{long_ex}* @ {long_price}\n"
        f"📉 Short на *{short_ex}* @ {short_price}\n"
        f"💰 Потенциальный PnL: *${pnl}*\n\n"
        f"_Используй /auto для авто-мониторинга_"
    )

    await message.answer(text, parse_mode="Markdown")
