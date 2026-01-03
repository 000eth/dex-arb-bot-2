import aiohttp
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://api.hyperliquid.xyz/info"


async def get_price(symbol: str):
    """
    Получает mark price с Hyperliquid.
    Hyperliquid возвращает ВСЕ монеты сразу, поэтому мы фильтруем нужную.
    """

    payload = {"type": "meta"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(BASE_URL, json=payload, timeout=5) as resp:
                data = await resp.json()
    except Exception as e:
        logger.warning(f"Hyperliquid request error: {e}")
        return None

    # Проверяем формат ответа
    if "universe" not in data:
        logger.warning(f"Hyperliquid unexpected response: {data}")
        return None

    # Ищем монету в списке
    for item in data["universe"]:
        if item.get("name") == symbol:
            try:
                return float(item["markPx"])
            except Exception as e:
                logger.warning(f"Hyperliquid parse error for {symbol}: {e}")
                return None

    # Монета не найдена
    logger.warning(f"Hyperliquid: symbol {symbol} not found in universe")
    return None
