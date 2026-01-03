from logic.models import ExchangeQuote

class PacificaExchange:
    name = 'Pacifica'

    async def get_quotes(self, symbol):
        return [ExchangeQuote('Pacifica', symbol, 121, 120.8, 121.2, 0.0002, 0.0005, -0.00002)]
