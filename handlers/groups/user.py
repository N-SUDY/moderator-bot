from load import bot, dp, types

import config

from load import database
from database.models import Member


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

@dp.message_handler(commands=["leave"],chat_type=[types.ChatType.SUPERGROUP])
async def leave_group(message:types.Message):
    user = message.from_user
    args = message.text.split()
    
    # TODO: translate it too
    if (len(args) < 1) or not ( ' '.join(args[1:]) == "I UNDERSTAND" ):
        await message.answer("Для того чтобы покинуть чат вам нужно ввести /leave I UNDERSTANT!")
        return
     
    database.delete_user(user.id)  

    # Ban user and save (bool)
    status = await bot.kick_chat_member(chat_id=message.chat.id,user_id=user.id,until_date=None)
    
    if status:
        await message.answer(f"User [{user.first_name}](tg://user?id={user.id}) has laved chat forever.",
            parse_mode="Markdown")

@dp.message_handler(commands=["start","help"],chat_type=[types.ChatType.SUPERGROUP])
async def start_command_group(message:types.Message):
    await message.answer((
        f"Hi,**{message.from_user.first_name}**!\n"
        "My commands:\n"
        "    /help , /start - read the message.\n"
        "    /me   , /bio   - member information (if member group)."),
        parse_mode="Markdown"
    )

@dp.message_handler(commands=["bio","me"],chat_type=[types.ChatType.SUPERGROUP])
async def get_information(message: types.Message):
    user = database.search_single_member(Member.user_id,message.from_user.id)
    
    role_level = config.roles["level"]

    if (user is None):
        await message.answer("❌Sorry,you not member group.")
        return 
    
    await message.answer((
        f"User:[{user.first_name}](tg://user?id={user.user_id})\n"
        f"level:{role_level[user.role]}\n"),
        parse_mode="Markdown"
    )

@dp.message_handler(commands=["report"],replied=True,chat_type=[types.ChatType.SUPERGROUP])
async def report(message: types.Message):
    args = message.text.split()
    
    if (len(args) != 2):
        await message.reply("Please,enter reason.")
        return

    reported_user = message.reply_to_message.from_user
    reporter_user = message.from_user
    reason = args[1] 
    
    # TODO: translate it
    msg = ("Жалоба на: [{}](tg://user?id={})\nПожаловался:[{}](tg://user?id={})\nПричина: {}\n{}"
    .format(reported_user['first_name'],
        reported_user['id'],
        reporter_user.first_name,
        reporter_user.id,
        reason,
        message.reply_to_message.link("Link message", as_html=False)
    ))
   
    await bot.send_message(config.telegram_log_chat_id, msg, parse_mode="Markdown")

@dp.message_handler(content_types=["left_chat_member"])
async def event_left_chat(message:types.Message):
    await message.delete()
