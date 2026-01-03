from logic.models import ExchangeQuote

class NadoExchange:
    name = 'Nado'

    async def get_quotes(self, symbol):
        return [ExchangeQuote('Nado', symbol, 120, 119.8, 120.2, 0.0002, 0.0005, 0.0001)]
