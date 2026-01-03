from typing import List, Optional
from .models import ExchangeQuote, ArbOpportunity

def compute_quantity(position_size, leverage, entry_price):
    return (position_size * leverage) / entry_price

def compute_fees_usd(position_notional, fee_open_long, fee_close_long, fee_open_short, fee_close_short):
    total_fee_rate = fee_open_long + fee_close_long + fee_open_short + fee_close_short
    return position_notional * total_fee_rate

def find_best_arb(quotes, symbol, position_size, leverage, min_pnl):
    filtered = [q for q in quotes if q.symbol == symbol]
    if len(filtered) < 2:
        return None

    best = None

    for long_q in filtered:
        for short_q in filtered:
            if long_q.exchange == short_q.exchange:
                continue

            entry_long = long_q.ask
            entry_short = short_q.bid
            if entry_long <= 0 or entry_short <= 0:
                continue

            mid = (entry_long + entry_short) / 2
            qty = compute_quantity(position_size, leverage, mid)
            notional = position_size * leverage

            spread = entry_short - entry_long
            gross = spread * qty

            fees = compute_fees_usd(
                notional,
                long_q.taker_fee, long_q.taker_fee,
                short_q.taker_fee, short_q.taker_fee
            )

            net = gross - fees
            spread_rel = spread / mid

            if net >= min_pnl:
                opp = ArbOpportunity(
                    long_exchange=long_q.exchange,
                    short_exchange=short_q.exchange,
                    symbol=symbol,
                    position_size=position_size,
                    leverage=leverage,
                    quantity=qty,
                    price_long=entry_long,
                    price_short=entry_short,
                    gross_pnl=gross,
                    fees=fees,
                    net_pnl=net,
                    spread_abs=spread,
                    spread_rel=spread_rel
                )
                if best is None or opp.net_pnl > best.net_pnl:
                    best = opp

    return best
