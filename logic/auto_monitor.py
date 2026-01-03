import asyncio
from logic.arbitrage import check_arbitrage

user_settings = {}

def get_user_settings(uid):
    if uid not in user_settings:
        user_settings[uid] = {
            "enabled": False,
            "interval": 5,
            "min_pnl": 1,
            "symbols": ["BTC"],
            "last_pnl": {},
            "next_check": 0
        }
    return user_settings[uid]


async def auto_monitor_loop(bot):
    while True:
        await asyncio.sleep(1)

        for uid, cfg in user_settings.items():
            if not cfg["enabled"]:
                continue

            # Если интервал изменился — сбрасываем таймер
            if cfg["next_check"] > cfg["interval"]:
                cfg["next_check"] = cfg["interval"]

            cfg["next_check"] -= 1

            if cfg["next_check"] > 0:
                continue

            # Сразу ставим новый интервал
            cfg["next_check"] = cfg["interval"]

            # Проверяем каждую монету
            for symbol in cfg["symbols"]:
                result = await check_arbitrage(symbol)

                if "error" in result:
                    continue

                pnl = result["pnl"]

                if pnl < cfg["min_pnl"]:
                    continue

                if cfg["last_pnl"].get(symbol) == pnl:
                    continue

                cfg["last_pnl"][symbol] = pnl

                text = (
                    f"📡 *Авто‑мониторинг*\n"
                    f"Монета: *{symbol}*\n\n"
                    f"🟢 Long: *{result['long']}* @ `{result['long_price']}`\n"
                    f"🔴 Short: *{result['short']}* @ `{result['short_price']}`\n"
                    f"💰 PnL: *{pnl}$*\n"
                )

                await bot.send_message(uid, text, parse_mode="Markdown")
