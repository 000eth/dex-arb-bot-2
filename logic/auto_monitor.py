import asyncio
from logic.arbitrage import check_arbitrage

user_settings = {}

def get_user_settings(uid):
    if uid not in user_settings:
        user_settings[uid] = {
            "enabled": False,
            "interval": 5,
            "min_pnl": 1,
            "symbol": "BTC",
            "last_pnl": None,
            "next_check": 0
        }
    return user_settings[uid]


async def auto_monitor_loop(bot):
    while True:
        await asyncio.sleep(1)

        for uid, cfg in user_settings.items():
            if not cfg["enabled"]:
                continue

            cfg["next_check"] -= 1
            if cfg["next_check"] > 0:
                continue

            cfg["next_check"] = cfg["interval"]

            result = await check_arbitrage(cfg["symbol"])

            if "error" in result:
                continue

            pnl = result["pnl"]

            if pnl < cfg["min_pnl"]:
                continue

            if cfg["last_pnl"] == pnl:
                continue

            cfg["last_pnl"] = pnl

            text = (
                f"📡 *Авто‑мониторинг*\n"
                f"Монета: *{cfg['symbol']}*\n\n"
                f"🟢 Long: *{result['long']}* @ `{result['long_price']}`\n"
                f"🔴 Short: *{result['short']}* @ `{result['short_price']}`\n"
                f"💰 PnL: *{pnl}$*\n"
            )

            await bot.send_message(uid, text, parse_mode="Markdown")
