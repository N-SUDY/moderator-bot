from load import dp,types, bot

from config import group_id

# TODO: channel post forward in chat
@dp.channel_post_handler()
async def channel_handler(message:types.Message):
    await message.forward(group_id)
