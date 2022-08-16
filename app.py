#!/usr/bin/env python3
import logging
from aiogram import executor
from database import models

from load import dp, bot
import filters

dp.filters_factory.bind(filters.AvaibleRolesFilter)
dp.filters_factory.bind(filters.ReplayMessageFilter)

import handlers
import config



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 3001

# Don`t touch anything!
WEBHOOK_HOST = f'http://{WEBAPP_HOST}:{WEBAPP_PORT}'
WEBHOOK_PATH = f'/bot{config.token}/'
WEBHOOK_URL =  f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

async def on_startup(dp):
    from utils.notify_start import notify_started_bot
    await notify_started_bot(bot)
    
    from utils.default_commands import set_default_commands
    await set_default_commands(dp)
    
    from load import tgc
    await tgc.client.start()

    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

    # Close Redis connection.
    await dp.storage.close()
    await dp.storage.wait_closed()

def main() -> None:
    models.build()

    if config.use_webhook:
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )

    else:
        executor.start_polling(dp,skip_updates=True)
            

if __name__ == '__main__':
    main()
