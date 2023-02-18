from load import dp, types
from config import group_id


@dp.channel_post()
async def channel_handler(message):
    await message.forward(group_id)
