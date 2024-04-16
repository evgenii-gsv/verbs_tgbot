from aiogram import F, Bot, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from verbs_tgbot.services.exceptions import InvalidAnswer
from verbs_tgbot.services.irregular_verbs import get_random_verbs_from_file
from verbs_tgbot.services.serializers import deserialize_verbs, serialize_verbs
from verbs_tgbot.services.utils import check_answers_and_get_response, notify_teacher, render_verbs
from verbs_tgbot.services import messages
from verbs_tgbot.config_reader import config


router = Router()

class CheckVerbs(StatesGroup):
    """States of the verbs challenge"""
    sending_verb_forms = State()


@router.message(Command('verbs'))
async def cmd_verbs(message: types.Message, state: FSMContext, bot: Bot):
    """A handler that will start the challenge on user request"""

    verbs = get_random_verbs_from_file()
    verbs_quantity = len(verbs)
    verbs_rendered = render_verbs(verbs)
    template = messages.NEW_VERBS.format(
        verbs_quantity=str(verbs_quantity),
        verbs=verbs_rendered
    )
    await message.answer(
        text=template
    )
    await notify_teacher(bot=bot, text=messages.TEACHER_NOTIF_VERBS_SENT.format(
                username=message.from_user.username if message.from_user else '',
                verbs=verbs_rendered 
            ))
    await state.update_data(verbs=serialize_verbs(verbs))
    await state.set_state(CheckVerbs.sending_verb_forms)


@router.message(CheckVerbs.sending_verb_forms, F.text)
async def verb_forms_sent(message: types.Message, state: FSMContext, bot: Bot):
    """A handler for checking the user's answer to verb challenge"""

    data = await state.get_data()
    verbs = deserialize_verbs(data['verbs'])
    redemption = data.get('redemption', False)
    try:
        reply, wrong_verbs = check_answers_and_get_response(verbs, message)
        await message.answer(text=reply)
        # sending notification to the teacher
        await bot.send_message(config.teacher_telegram_id, text=messages.TEACHER_NOTIF_VERBS_ANSWER_RECEIVED.format(
            username=message.from_user.username if message.from_user else '',
            result=reply
        ))
        # if there are wrong answers, we continue the challenge but only with wrong verbs
        if wrong_verbs:
            await state.update_data(verbs=serialize_verbs(wrong_verbs))
            # adding wrong verbs to the list of error verbs
            if not redemption:
                error_verbs = deserialize_verbs(data['error_verbs']) if data.get('error_verbs') else []
                error_verbs.extend(verb for verb in wrong_verbs if verb not in error_verbs)
                await state.update_data(error_verbs=serialize_verbs(error_verbs))
        # if there are no wrong ansers, we finish the challenge
        else:
            if redemption:
                await state.clear()
            else:
                await state.set_state(state=None)
            
    except InvalidAnswer:
        await message.answer(text=messages.INVALID_ANSWER.format(verbs_quantity=str(len(verbs))))
