import aiohttp

BASE_URL = "https://api.hyperliquid.xyz"

async def get_price(symbol: str) -> float:
    """
    Получает цену через l2Book (стакан).
    Работает для всех активов Hyperliquid.
    """

    url = f"{BASE_URL}/info"
    payload = {
        "type": "l2Book",
        "coin": symbol.upper()
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            data = await resp.json()

    # Проверяем структуру ответа
    if "levels" not in data:
        raise ValueError(f"Unexpected response: {data}")

    bids = data["levels"]["bids"]
    asks = data["levels"]["asks"]

    if not bids or not asks:
        raise ValueError(f"No orderbook data for {symbol}")

    best_bid = float(bids[0][0])
    best_ask = float(asks[0][0])

    # Возвращаем среднюю цену
    return (best_bid + best_ask) / 2
