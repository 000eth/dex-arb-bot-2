import asyncio
from logic.arbitrage import check_arbitrage

# Храним настройки пользователей
user_settings = {}  # uid -> {enabled, interval, min_pnl, symbol, last_pnl}

def get_user_settings(uid):
    if uid not in user_settings:
        user_settings[uid] = {
            "enabled": False,
            "interval": 5,      # интервал проверки в секундах
            "min_pnl": 1,       # минимальный профит для сигнала
            "symbol": "BTC",    # монета
            "last_pnl": None    # чтобы не спамить одинаковыми сигналами
        }
    return user_settings[uid]


async def auto_monitor_loop(bot):
    """
    Фоновая задача, которая крутится всегда.
    Проверяет арбитраж для всех пользователей, у кого включён авто‑мониторинг.
    """
    while True:
        await asyncio.sleep(1)

        for uid, cfg in user_settings.items():
            if not cfg["enabled"]:
                continue

            # Проверяем раз в cfg["interval"] секунд
            if "next_check" not in cfg:
                cfg["next_check"] = 0

            cfg["next_check"] -= 1
            if cfg["next_check"] > 0:
                continue

            cfg["next_check"] = cfg["interval"]

            result = await check_arbitrage(cfg["symbol"])

            if "error" in result:
                continue

            pnl = result["pnl"]

            # Если профит меньше минимального — пропускаем
            if pnl < cfg["min_pnl"]:
                continue

            # Если сигнал такой же, как предыдущий — не спамим
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
