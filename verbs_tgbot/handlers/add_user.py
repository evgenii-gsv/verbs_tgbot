from aiogram import Router, types
from aiogram.filters import Command

from verbs_tgbot.services import messages
from verbs_tgbot.services.utils import add_user_to_file
from verbs_tgbot.config_reader import config


router = Router()


@router.message(Command('start'))
async def add_user_to_verbs_challenge(message: types.Message):
    """A handler to add user to verbs challenge"""
    
    if message.from_user:
        time_of_challenge = str(config.verbs_challenge_hour).rjust(2, '0') + ':' + \
        str(config.verbs_challenge_minute).rjust(2, '0')

        user, added = add_user_to_file(
            message.from_user.model_dump()
            )
        if added:
            await message.answer(
                text=messages.WELCOME_VERBS_CHALLENGE.format(
                    name = user['first_name'],
                    verbs_quantity = config.verbs_quantity_per_message,
                    time=time_of_challenge
                ))
        else:
            await message.answer(
                text=messages.SECOND_WELCOME_VERBS_CHALLENGE.format(
                    time=time_of_challenge
                )                
            )     
