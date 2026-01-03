# logic/exchange_links.py

def get_exchange_link(exchange: str, symbol: str) -> str:
    exchange = exchange.lower()

    # === ТВОИ РЕФЕРАЛКИ ===
    if exchange == "okx":
        return "https://okx.com/join/9188608"

    if exchange == "pacifica":
        return "https://app.pacifica.fi?referral=leaderboard"

    # === Дефолтные ссылки (если биржа без рефки) ===
    if exchange == "hyperliquid":
        return f"https://app.hyperliquid.xyz/trade/{symbol}"

    if exchange == "binance":
        return f"https://www.binance.com/en/trade/{symbol}_USDT"

    if exchange == "nado":
        return f"https://app.nado.xyz/trade/{symbol}"

    # fallback
    return "https://google.com"
