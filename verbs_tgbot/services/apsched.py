from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from verbs_tgbot.services import messages
from verbs_tgbot.config_reader import config
from verbs_tgbot.handlers.check_verbs import CheckVerbs
from verbs_tgbot.services.irregular_verbs import get_random_verbs_from_file
from verbs_tgbot.services.utils import get_users_from_file


async def add_all_jobs(bot: Bot, dp: Dispatcher, scheduler: AsyncIOScheduler):
    """This function will start all the jobs inside it on bot start up."""
    scheduler.add_job(
        send_verbs, 
        trigger='cron', 
        hour=config.verbs_challenge_hour, 
        minute=config.verbs_challenge_minute,
        kwargs={'bot': bot, 'dp': dp}
        )


async def send_verbs(bot: Bot, dp: Dispatcher):
    """This job will send verbs to a verbs challaenge participant on regular basis."""
    
    # checking if there are any users registered in the challenge 
    if config.verb_challenge_users_file.exists():
        users = get_users_from_file()
        for user in users:
            # getting the FSMContext of a participant
            state = FSMContext(
                storage=dp.storage,
                key=StorageKey(
                    chat_id=user['id'],
                    user_id=user['id'],
                    bot_id=bot.id
                )
            )
            verbs = get_random_verbs_from_file()
            verbs_quantity = len(verbs)
            verbs_rendered = '\n'.join('- to ' + verb.first_form for verb in verbs)
            template = messages.NEW_VERBS.format(
                verbs_quantity=str(verbs_quantity),
                verbs=verbs_rendered
            )
            await bot.send_message(
                chat_id=user['id'],
                text=template
            )
            # sendin notification to the teacher
            await bot.send_message(config.teacher_telegram_id, text=messages.TEACHER_NOTIF_VERBS_SENT.format(
                username=user['username'],
                verbs=verbs_rendered 
            ))
            await state.set_state(CheckVerbs.sending_verb_forms)
            await state.update_data(verbs=verbs)
