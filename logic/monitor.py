from exchanges import EXCHANGES

async def fetch_all_quotes(symbol):
    quotes = []
    for ex in EXCHANGES:
        try:
            q = await ex.get_quotes(symbol)
            quotes.extend(q)
        except Exception as e:
            print(f'Error fetching from {ex.name}: {e}')
    return quotes
