from exchanges.hyperliquid import get_price as hl_price
from exchanges.binance import get_price as binance_price
from exchanges.okx import get_price as okx_price

import logging

logger = logging.getLogger(__name__)

async def check_arbitrage(symbol: str):
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
        "hyperliquid": hl,
        "binance": binance,
        "okx": okx,
    }

    # Убираем биржи, где нет цены
    clean = {ex: p for ex, p in prices.items() if p is not None}

    if len(clean) < 2:
        return {"error": "Недостаточно данных для арбитража"}

    # --- Ищем лучший и худший курс ---
    best_ex = max(clean, key=clean.get)
    worst_ex = min(clean, key=clean.get)

    spread = clean[best_ex] - clean[worst_ex]

    return {
        "best_exchange": best_ex,
        "best_price": clean[best_ex],
        "worst_exchange": worst_ex,
        "worst_price": clean[worst_ex],
        "spread": spread,
        "all_prices": clean
    }
