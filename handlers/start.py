from aiogram import Router, types
from aiogram.filters import Command

from keyboards import main_menu

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Бот запущен. Выбирай действие:",
        reply_markup=main_menu
    )
