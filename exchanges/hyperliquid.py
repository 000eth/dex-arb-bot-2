import aiohttp

BASE_URL = "https://api.hyperliquid.xyz"

async def get_price(symbol: str) -> float:
    """
    Получает последнюю цену по инструменту.
    symbol: например 'BTC', 'ETH'
    """
    url = f"{BASE_URL}/info"
    payload = {
        "type": "metaAndAssetCtxs"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            data = await resp.json()

    assets = data.get("assetCtxs", [])
    for asset in assets:
        if asset["name"].upper() == symbol.upper():
            return float(asset["markPx"])

    raise ValueError(f"Symbol {symbol} not found on Hyperliquid")


async def get_orderbook(symbol: str):
    """
    Получает стакан (best bid / best ask)
    """
    url = f"{BASE_URL}/info"
    payload = {
        "type": "l2Book",
        "coin": symbol.upper()
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            data = await resp.json()

    bids = data["levels"]["bids"]
    asks = data["levels"]["asks"]

    best_bid = float(bids[0][0])
    best_ask = float(asks[0][0])

    return best_bid, best_ask
