import aiohttp

BASE_URL = "https://www.okx.com/api/v5/market/ticker"

async def get_price(symbol: str) -> float:
    """
    Получает среднюю цену (mid price) с OKX.
    symbol: 'BTC', 'ETH', 'SOL' и т.д.
    """
    url = f"{BASE_URL}?instId={symbol.upper()}-USDT-SWAP"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    if "data" not in data or not data["data"]:
        raise ValueError(f"OKX error: {data}")

    ticker = data["data"][0]

    bid = float(ticker["bidPx"])
    ask = float(ticker["askPx"])

    return (bid + ask) / 2
