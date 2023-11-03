from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from verbs_tgbot.services import messages
from verbs_tgbot.config_reader import config
from verbs_tgbot.handlers.check_verbs import CheckVerbs
from verbs_tgbot.services.irregular_verbs import get_random_verbs_from_file
from verbs_tgbot.services.serializers import deserialize_verbs, serialize_verbs
from verbs_tgbot.services.utils import get_fsmcontext_of_user, get_redemption_template, get_users_from_file, notify_teacher, render_verbs


async def add_all_jobs(bot: Bot, dp: Dispatcher, scheduler: AsyncIOScheduler):
    """This function will start all the jobs inside it on bot start up."""
    scheduler.add_job(
        send_verbs, 
        trigger='cron', 
        hour=config.verbs_challenge_hour, 
        minute=config.verbs_challenge_minute,
        day_of_week=config.verbs_challenge_days,
        kwargs={'bot': bot, 'dp': dp}
        )
    scheduler.add_job(
        send_verbs_redemption, 
        trigger='cron', 
        hour=config.verbs_challenge_hour, 
        minute=config.verbs_challenge_minute,
        day_of_week=config.redemption_verbs_challenge_day,
        kwargs={'bot': bot, 'dp': dp}
        )


async def send_verbs(bot: Bot, dp: Dispatcher):
    """This job will send verbs to a verbs challenge participant daily."""
    
    # checking if there are any users registered in the challenge 
    if not config.verb_challenge_users_file.exists():
        return

    users = get_users_from_file()
    for user in users:
        # getting the FSMContext of a participant
        state = get_fsmcontext_of_user(user, dp, bot)
        verbs = get_random_verbs_from_file()
        verbs_quantity = len(verbs)
        verbs_rendered = render_verbs(verbs)
        template = messages.NEW_VERBS.format(
            verbs_quantity=str(verbs_quantity),
            verbs=verbs_rendered
        )
        await bot.send_message(
            chat_id=user['id'],
            text=template
        )
        # sending notification to the teacher
        await notify_teacher(bot=bot, text=messages.TEACHER_NOTIF_VERBS_SENT.format(
            username=user['username'],
            verbs=verbs_rendered 
        ))
        await state.set_state(CheckVerbs.sending_verb_forms)
        await state.update_data(verbs=serialize_verbs(verbs))


async def send_verbs_redemption(bot: Bot, dp: Dispatcher):
    """This job will send verbs to a verbs challenge participant weekly based on their errors."""
    
    # checking if there are any users registered in the challenge 
    if not config.verb_challenge_users_file.exists():
        return
    
    users = get_users_from_file()
    for user in users:
        # getting the FSMContext of a participant
        state = get_fsmcontext_of_user(user, dp, bot)
        data = await state.get_data()
        verbs = deserialize_verbs(data['error_verbs']) if data.get('error_verbs') else []
        error_verbs_quantity = len(verbs)

        # check if the quantity of errors is less than verbs_quantity_per_message, if so, add new verbs to get to the desired amount
        if error_verbs_quantity < config.verbs_quantity_per_message:
            verbs.extend(get_random_verbs_from_file(
                verbs_quantity=config.verbs_quantity_per_message - error_verbs_quantity
                ))
        
        verbs_rendered = render_verbs(verbs)
        template = get_redemption_template(error_verbs_quantity, len(verbs), verbs_rendered)

        await bot.send_message(
            chat_id=user['id'],
            text=template
        )
        # sending notification to the teacher
        await notify_teacher(bot=bot, text=messages.TEACHER_NOTIF_VERBS_SENT_REDEMPTION.format(
            username=user['username'],
            error_verbs_quantity = str(error_verbs_quantity),
            verbs=verbs_rendered
        ))
        await state.set_state(CheckVerbs.sending_verb_forms)
        await state.update_data(verbs=serialize_verbs(verbs), redemption=True)
