from load import dp, bot, types

# TODO: fix it
# import utils
# import config
# vt = utils.VirusTotalAPI(config.vt_api,True)
# @dp.message_handler(content_types=["document"],chat_type=[types.ChatType.SUPERGROUP])
# async def file_handler(message:types.Message): 
#     file = await bot.get_file(message.document.file_id)
#
#     await bot.send_message(
#         message.chat.id,
#         await vt.scan_file(file.file_path),
#         parse_mode="Markdown"
#     )

@dp.message_handler()
async def filter_link_shorts(message:types.Message):
    link_shorters = open("txt/link_shorters.txt","r").read().split()
    
    for y in link_shorters:
        for user_message in message.text.lower().split():
            if (y in user_message):await message.delete()

# Joke
@dp.message_handler(content_types=types.ContentType.VOICE)
async def voice_message(message:types.Message):
    photo = types.InputFile(path_or_bytesio="media/photo.jpg")
    await message.answer_photo(photo)
