from aiogram import Router, types, F
from keyboards import main_menu

router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer(
        "Добро пожаловать! Выбирай действие:",
        reply_markup=main_menu
    )
