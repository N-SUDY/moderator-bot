import logging

from peewee import DoesNotExist

from load import dp, bot, types
import config

from aiogram.utils.exceptions import Unauthorized


@dp.errors_handler()
async def errors_handler(update: types.Update, exception):
    if (isinstance(exception, Unauthorized)):
        logging.info(f"Unathorized:{config.token}")
        return True
    
    if (isinstance(exception, DoesNotExist)):
        await update.message.reply("Membser not found, you shoud update database data `!reload`",
            parse_mode="Markdown")
        return True

    await update.message.answer("Error happaned!\nBot terminated!")

    await bot.send_message(config.second_group_id, (
            "Bot terminated"
            f"{exception}"
        ), parse_mode="Markdown"
    )
