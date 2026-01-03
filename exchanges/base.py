from abc import ABC, abstractmethod
from typing import List
from logic.models import ExchangeQuote

class BaseExchange(ABC):
    name: str

    @abstractmethod
    async def get_quotes(self, symbol: str) -> List[ExchangeQuote]:
        pass
