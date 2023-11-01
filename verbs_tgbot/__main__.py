import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from verbs_tgbot.services.apsched import add_all_jobs

from verbs_tgbot.config_reader import config
from verbs_tgbot.handlers import check_verbs, add_user, ping


async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    bot = Bot(token=config.bot_token.get_secret_value())
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    dp = Dispatcher(scheduler=scheduler)
    scheduler.start()

    dp.include_routers(
        check_verbs.router, 
        add_user.router,
        ping.router
        )

    # starting all initial jobs of apscheduler
    await add_all_jobs(bot, dp, scheduler)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())