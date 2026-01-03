from exchanges.hyperliquid import get_price as hl_price
from exchanges.binance import get_price as binance_price
from exchanges.okx import get_price as okx_price

import logging
logger = logging.getLogger(__name__)

async def check_arbitrage(symbol: str = "ETH"):
    """
    Проверяет арбитраж между Hyperliquid, Binance и OKX.
    Возвращает словарь с результатами.
    """

    # --- Получаем цены с бирж ---
    try:
        hl = await hl_price(symbol)
    except Exception as e:
        hl = None
        logger.warning(f"Hyperliquid error: {e}")

    try:
        binance = await binance_price(symbol)
    except Exception as e:
        binance = None
        logger.warning(f"Binance error: {e}")

    try:
        okx = await okx_price(symbol)
    except Exception as e:
        okx = None
        logger.warning(f"OKX error: {e}")

    # --- Собираем цены ---
    prices = {
        "Hyperliquid": hl,
        "Binance": binance,
        "OKX": okx
    }

    # Убираем биржи, где нет цены
    clean = {ex: p for ex, p in prices.items() if p is not None}

    if len(clean) < 2:
        return {"error": "Недостаточно данных для арбитража"}

    # --- Ищем лучший и худший курс ---
    long_ex = min(clean, key=clean.get)
    short_ex = max(clean, key=clean.get)

    long_price = clean[long_ex]
    short_price = clean[short_ex]
    pnl = round(short_price - long_price, 2)

    return {
        "long": long_ex,
        "short": short_ex,
        "long_price": long_price,
        "short_price": short_price,
        "pnl": pnl,
        "all_prices": clean
    }
