import config

async def notify_started_bot(bot):
    await bot.send_message(config.second_group_id,"Bot started!")
