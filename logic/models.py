from dataclasses import dataclass
from typing import Optional

@dataclass
class ExchangeQuote:
    exchange: str
    symbol: str
    price: float
    bid: float
    ask: float
    maker_fee: float
    taker_fee: float
    funding_rate_hourly: Optional[float] = None

@dataclass
class ArbOpportunity:
    long_exchange: str
    short_exchange: str
    symbol: str
    position_size: float
    leverage: float
    quantity: float
    price_long: float
    price_short: float
    gross_pnl: float
    fees: float
    net_pnl: float
    spread_abs: float
    spread_rel: float
