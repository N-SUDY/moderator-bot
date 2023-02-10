#!/usr/bin/env python3
import logging

from load import dp, bot, scheduler

from aiohttp.web_app import Application
from aiohttp.web import run_app
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application
)


# import filters
import config


# dp.filters_factory.bind(filters.AvaibleRolesFilter)
# dp.filters_factory.bind(filters.ReplayMessageFilter)

# import handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 3001

# Don`t touch anything!
WEBHOOK_HOST = f'http://{WEBAPP_HOST}:{WEBAPP_PORT}'
WEBHOOK_PATH = f'/bot{config.token}/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


async def on_startup():
    from utils.notify_start import notify_started_bot, database_is_empty
    
    DATABASE_EMPTY = database_is_empty()
    if DATABASE_EMPTY:
        await bot.send_message(
            config.second_group_id,
            "Member table is empty, run: `!reload`", parse_mode="Markdown"
        )

    await notify_started_bot(bot)
     
    from utils.default_commands import set_default_commands
    await set_default_commands(bot)
    
    # Reloading users data
    from utils import reload_users_data
    scheduler.add_job(reload_users_data, "interval", seconds=config.update_interval)
    scheduler.start()

    from load import tgc
    await tgc.client.start()
    
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown():
    await bot.delete_webhook()

    # Close Redis connection.
    await dp.storage.close()
    await bot.session.close()

    
def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    if config.USE_WEBHOOK:
        app = Application()
        app["bot"] = bot
        SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        ).register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
    else:
        dp.run_polling()


if __name__ == '__main__':
    main()
