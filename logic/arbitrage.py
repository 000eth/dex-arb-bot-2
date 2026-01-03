from exchanges.hyperliquid import get_price as hl_price

import logging
logger = logging.getLogger(__name__)

async def check_arbitrage(symbol: str = "BTC"):
    try:
        hl = await hl_price(symbol)
    except Exception as e:
        hl = None
        logger.warning(f"Hyperliquid error: {e}")
        return {"error": f"Hyperliquid API error: {e}"}

    if hl is None:
        return {"error": "Не удалось получить цену Hyperliquid"}

    return {
        "long": "Hyperliquid",
        "short": "Hyperliquid",
        "long_price": hl,
        "short_price": hl + 1,
        "pnl": 1,
        "all_prices": {"Hyperliquid": hl}
    }
