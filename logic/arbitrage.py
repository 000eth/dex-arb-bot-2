from exchanges.hyperliquid import get_price as hl_price

import logging
logger = logging.getLogger(__name__)

async def check_arbitrage(symbol: str = "ETH"):
    """
    Проверяет цену на Hyperliquid.
    Возвращает фейковый арбитраж для демонстрации.
    """

    try:
        hl = await hl_price(symbol)
    except Exception as e:
        hl = None
        logger.warning(f"Hyperliquid error: {e}")

    if hl is None:
        return {"error": "Не удалось получить цену Hyperliquid"}

    # Для теста: считаем, что арбитраж = цена + 1$
    return {
        "long": "Hyperliquid",
        "short": "Hyperliquid",
        "long_price": hl,
        "short_price": hl + 1,
        "pnl": 1,
        "all_prices": {"Hyperliquid": hl}
    }
