from load import dp, database, types
from database.models import Member


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

@dp.message_handler(content_types=["new_chat_members"])
async def welcome_message(message:types.Message):
    # User
    user = message.from_user 
    
    exists = database.check_data_exists(Member.user_id,user.id)
    
    if (exists):
        await message.answer("Спасибо что вы с нами.")

    if not (exists):
        database.register_user(user.id,user.first_name,user.username)
        # TODO: translate it    
        await message.answer((
            f"Привет,{user.first_name}\n"
            "Просим ознакомится с [правилами](https://telegra.ph/Pravila-CHata-Open-Source-05-29)\n"
            "Советы на 'хороший тон':\n"
            "\t\t1.Формулируй свою мысль в 1-2 предложения\n"
            "\t\t1.Не задавай [мета](nometa.xyz) вопросы\n"),
        parse_mode="Markdown")
    

    await message.delete()

# @dp.message_handler()
# async def filter_link_shorts(message:types.Message):
#     link_shorters = open("txt/link_shorters.txt","r").read().split()
#     
#     for y in link_shorters:
#         for user_message in message.text.lower().split():
#             if (y in user_message):await message.delete()

# Joke
@dp.message_handler(content_types=types.ContentType.VOICE)
async def voice_message(message:types.Message):
    photo = types.InputFile(path_or_bytesio="media/photo.jpg")
    await message.answer_photo(photo)
