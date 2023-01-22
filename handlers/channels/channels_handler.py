from load import dp, types
from config import group_id


@dp.channel_post_handler()
async def channel_handler(message: types.Message):
    await message.forward(group_id)
