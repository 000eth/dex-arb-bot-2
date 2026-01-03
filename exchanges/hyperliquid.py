import aiohttp

BASE_URL = "https://api.hyperliquid.xyz"

async def get_price(symbol: str) -> float:
    url = f"{BASE_URL}/info"
    payload = {
        "type": "metaAndAssetCtxs"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            data = await resp.json()

    # Hyperliquid возвращает список, берём первый элемент
    if isinstance(data, list) and len(data) > 0:
        assets = data[0].get("assetCtxs", [])
        for asset in assets:
            if asset["name"].upper() == symbol.upper():
                return float(asset["markPx"])

    raise ValueError(f"Symbol {symbol} not found on Hyperliquid")
