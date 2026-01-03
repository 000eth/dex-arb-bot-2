from logic.models import ExchangeQuote

class VariationalExchange:
    name = 'Variational'

    async def get_quotes(self, symbol):
        return [ExchangeQuote('Variational', symbol, 120.8, 120.6, 121, 0.0003, 0.0006, 0)]
