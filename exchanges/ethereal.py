from logic.models import ExchangeQuote

class EtherealExchange:
    name = 'Ethereal'

    async def get_quotes(self, symbol):
        return [ExchangeQuote('Ethereal', symbol, 120.5, 120.3, 120.7, 0.0002, 0.0005, 0.00005)]
