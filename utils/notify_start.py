import config

async def notify_started_bot(bot):
    await bot.send_message(config.telegram_log_chat_id,"Bot started!")
