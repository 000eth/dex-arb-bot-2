import aiohttp

BASE_URL = "https://api.binance.com/api/v3/ticker/bookTicker"

async def get_price(symbol: str) -> float:
    """
    Получает среднюю цену (mid price) с Binance.
    symbol: 'BTC', 'ETH', 'SOL' и т.д.
    """
    url = f"{BASE_URL}?symbol={symbol.upper()}USDT"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    if "bidPrice" not in data:
        raise ValueError(f"Binance error: {data}")

    bid = float(data["bidPrice"])
    ask = float(data["askPrice"])

    return (bid + ask) / 2
