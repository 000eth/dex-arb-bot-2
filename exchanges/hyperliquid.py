import aiohttp
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://api.hyperliquid.xyz/info"


async def get_price(symbol: str):
    """
    Получает mark price с Hyperliquid.
    Hyperliquid возвращает ВСЕ монеты сразу, мы ищем нужную.
    """

    payload = {"type": "meta"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(BASE_URL, json=payload, timeout=5) as resp:
                data = await resp.json()
    except Exception as e:
        logger.warning(f"Hyperliquid request error: {e}")
        return None

    # Проверяем наличие universe
    universe = data.get("universe")
    if not universe or not isinstance(universe, list):
        logger.warning(f"Hyperliquid unexpected response format: {data}")
        return None

    # Ищем нужную монету
    for item in universe:
        if item.get("name") == symbol:
            mark_px = item.get("markPx")
            if mark_px is None:
                logger.warning(f"Hyperliquid: markPx missing for {symbol}")
                return None
            try:
                return float(mark_px)
            except Exception as e:
                logger.warning(f"Hyperliquid parse error for {symbol}: {e}")
                return None

    logger.warning(f"Hyperliquid: symbol {symbol} not found in universe")
    return None
