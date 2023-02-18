import logging

from load import dp, bot, types
import config

from peewee import DoesNotExist
from aiogram.exceptions import TelegramUnauthorizedError


@dp.errors()
async def errors_handler(event: types.error_event.ErrorEvent):
    if (isinstance(event.exception, TelegramUnauthorizedError)):
        logging.info(f"Unathorized: {config.token}")
        return True
    
    if (isinstance(event.exception, DoesNotExist)):
        event.update.message.reply("Membser not found, you shoud update database data `!reload`")
        return True
    
    await bot.send_message(config.second_group_id, (
        "Bot terminated\n"
        f"Exception: {event.exception}"
    ))
