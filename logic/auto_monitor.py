import asyncio
import time
from logic.arbitrage import check_arbitrage

# Храним настройки по пользователям
user_settings: dict[int, dict] = {}


def get_user_settings(uid: int) -> dict:
    if uid not in user_settings:
        user_settings[uid] = {
            "enabled": False,     # авто-мониторинг выключен по умолчанию
            "interval": 5,        # интервал в секундах
            "min_pnl": 1,
            "symbols": ["BTC"],
            "last_pnl": {},       # pnl по каждой монете
            "last_check_ts": 0.0  # время последней проверки
        }
    return user_settings[uid]


async def auto_monitor_loop(bot):
    while True:
        now = time.time()

        for uid, cfg in user_settings.items():
            if not cfg["enabled"]:
                continue

            interval = cfg.get("interval", 5)
            last_check_ts = cfg.get("last_check_ts", 0.0)

            # Если ещё не прошло interval секунд — ждём
            if now - last_check_ts < interval:
                continue

            # Фиксируем время проверки сразу
            cfg["last_check_ts"] = now

            # Проверяем каждую монету
            for symbol in cfg["symbols"]:
                result = await check_arbitrage(symbol)

                if "error" in result:
                    continue

                pnl = result["pnl"]

                # Фильтр по min_pnl
                if pnl < cfg["min_pnl"]:
                    continue

                # Не спамим одинаковыми значениями
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

        # Глобальный тик цикла
        await asyncio.sleep(1)
