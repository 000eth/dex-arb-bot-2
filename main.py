import asyncio
from contextlib import suppress
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import settings
from logic.monitor import fetch_all_quotes
from logic.analyzer import find_best_arb

BOT_SYMBOL = 'SOL'
user_settings = {}

def get_user_settings(uid):
    if uid not in user_settings:
        user_settings[uid] = {
            'position_size': settings.DEFAULT_POSITION_SIZE,
            'leverage': settings.DEFAULT_LEVERAGE,
            'min_pnl': settings.DEFAULT_MIN_PNL,
            'auto_monitor': False
        }
    return user_settings[uid]

async def format_opp(opp):
    return f'Arbitrage opportunity: Long {opp.long_exchange} @ {opp.price_long}, Short {opp.short_exchange} @ {opp.price_short}, PnL {opp.net_pnl:.2f}$'

async def auto_loop(bot):
    while True:
        await asyncio.sleep(settings.DEFAULT_CHECK_INTERVAL_SEC)
        quotes = await fetch_all_quotes(BOT_SYMBOL)
        for uid, s in user_settings.items():
            if not s['auto_monitor']:
                continue
            opp = find_best_arb(quotes, BOT_SYMBOL, s['position_size'], s['leverage'], s['min_pnl'])
            if opp:
                with suppress(Exception):
                    await bot.send_message(uid, await format_opp(opp))

async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(Command('start'))
    async def start(m: Message):
        await m.answer('Bot is running. Use /check')

    @dp.message(Command('check'))
    async def check(m: Message):
        s = get_user_settings(m.from_user.id)
        quotes = await fetch_all_quotes(BOT_SYMBOL)
        opp = find_best_arb(quotes, BOT_SYMBOL, s['position_size'], s['leverage'], s['min_pnl'])
        if opp:
            await m.answer(await format_opp(opp))
        else:
            await m.answer('No opportunities.')

    asyncio.create_task(auto_loop(bot))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
