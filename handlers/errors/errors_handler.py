import logging

from load import dp,bot
import config

from aiogram.utils.exceptions import Unauthorized


@dp.errors_handler()
async def errors_handler(update, exception):
    if (isinstance(exception,Unauthorized)):
        logging.info(f"Unathorized:{config.token}")
        return True

    await update.message.answer("Error happaned!\nBot terminated!")

    await bot.send_message(
        config.second_group_id,
        f"**Bot terminated**!\nException:{exception}",
        parse_mode="Markdown"
    )

    logging.info(f"Bot terminated!")
