from aiogram import Router, types
from aiogram.filters import Command

from verbs_tgbot.services import messages


router = Router()

@router.message(Command('ping'))
async def ping(message: types.Message):
    await message.answer(text=messages.PING_RESPONSE)