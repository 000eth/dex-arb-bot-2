from logic.models import ExchangeQuote

class ExtendedExchange:
    name = 'Extended'

    async def get_quotes(self, symbol):
        return [ExchangeQuote('Extended', symbol, 119.7, 119.5, 119.9, 0.00025, 0.0006, 0.00008)]
