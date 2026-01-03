def get_exchange_link(exchange: str, symbol: str) -> str:
    symbol = symbol.upper()

    if exchange == "Hyperliquid":
        return f"https://app.hyperliquid.xyz/trade/{symbol}"

    if exchange == "Binance":
        return f"https://www.binance.com/en/trade/{symbol}_USDT"

    if exchange == "OKX":
        return f"https://www.okx.com/trade-swap/{symbol}-USDT-SWAP"

    return ""
