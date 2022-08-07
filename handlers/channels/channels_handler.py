from load import dp,types

# TODO: channel post forward in chat
@dp.channel_post_handler()
async def channel_handler(message:types.Message):
    print(message.text)
