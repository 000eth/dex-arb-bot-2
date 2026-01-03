import aiohttp
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://www.okx.com"


async def get_price(symbol: str):
    """
    Получает цену с OKX для фьючерса USDT-SWAP.
    Пример инструмента: BTC-USDT-SWAP, ETH-USDT-SWAP, SOL-USDT-SWAP
    """

    instrument = f"{symbol}-USDT-SWAP"
    url = f"{BASE_URL}/api/v5/market/ticker?instId={instrument}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                data = await resp.json()

    except Exception as e:
        logger.warning(f"OKX request error: {e}")
        return None

    # Проверяем формат ответа
    if "data" not in data or not data["data"]:
        logger.warning(f"OKX empty response for {instrument}: {data}")
        return None

    item = data["data"][0]

    # OKX возвращает цену как строку
    try:
        price = float(item["last"])
        return price
    except Exception as e:
        logger.warning(f"OKX parse error for {instrument}: {e}")
        return None
