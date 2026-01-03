import aiohttp

BASE_URL = "https://api.hyperliquid.xyz"

async def get_price(symbol: str) -> float:
    """
    Получает цену через l2Book (стакан).
    Работает с реальной структурой ответа Hyperliquid.
    """

    url = f"{BASE_URL}/info"
    payload = {
        "type": "l2Book",
        "coin": symbol.upper()
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            data = await resp.json()

    # Проверяем, что пришёл словарь
    if not isinstance(data, dict):
        raise ValueError(f"Unexpected response format: {data}")

    if "levels" not in data:
        raise ValueError(f"No levels in response: {data}")

    levels = data["levels"]

    # levels = [bids, asks]
    if len(levels) < 2:
        raise ValueError(f"Invalid levels structure: {levels}")

    bids = levels[0]
    asks = levels[1]

    if not bids or not asks:
        raise ValueError(f"No orderbook data for {symbol}")

    # bids и asks — это списки словарей {'px': '89990.0', ...}
    best_bid = float(bids[0]["px"])
    best_ask = float(asks[0]["px"])

    # Возвращаем среднюю цену
    return (best_bid + best_ask) / 2
