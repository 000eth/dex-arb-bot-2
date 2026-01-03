import aiohttp

BASE_URL = "https://api.hyperliquid.xyz"

async def get_price(symbol: str) -> float:
    """
    Получает цену через l2Book (стакан).
    Hyperliquid возвращает список, поэтому data[0].
    """

    url = f"{BASE_URL}/info"
    payload = {
        "type": "l2Book",
        "coin": symbol.upper()
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            data = await resp.json()

    # Проверяем, что пришёл список
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError(f"Unexpected response format: {data}")

    # Берём первый элемент
    item = data[0]

    if "levels" not in item:
        raise ValueError(f"No levels in response: {item}")

    bids = item["levels"]["bids"]
    asks = item["levels"]["asks"]

    if not bids or not asks:
        raise ValueError(f"No orderbook data for {symbol}")

    best_bid = float(bids[0][0])
    best_ask = float(asks[0][0])

    # Возвращаем среднюю цену
    return (best_bid + best_ask) / 2
