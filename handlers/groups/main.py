from load import bot, dp, types

import config
from database import Member


@dp.message_handler(
    commands=["start", "help"],
    chat_type=[types.ChatType.SUPERGROUP]
)
async def start_command_group(message: types.Message):
    await message.answer((
        f"Hi,**{message.from_user.first_name}**!\n"
        "My commands:\n"
        "    /help , /start - read the message\n"
        "    /me   , /bio   - member information (if member group)"),
        parse_mode="Markdown"
    )


@dp.message_handler(
    commands=["leave"],
    chat_type=[types.ChatType.SUPERGROUP]
)
async def leave_group(message: types.Message):
    user = message.from_user

    if (message.text.split()[0] != "I UNDERSTAND!"):
        await message.answer("use /leave I UNDERSTAND")
        return

    Member.delete().get(Member.user_id == user.id)

    status = await bot.kick_chat_member(
        chat_id=message.chat.id,
        user_id=user.id,
        until_date=None
    )
    
    if status:
        await message.answer((
            f"User [{user.first_name}](tg://user?id={user.id})"
            "has leaved chat for forever"
            ), parse_mode="Markdown"
        )
    
    Member.delete().where(Member.user_id == user.id).execute()


@dp.message_handler(
    commands=["bio", "me"],
    chat_type=[types.ChatType.SUPERGROUP]
)
async def get_information(message: types.Message):
    user = Member.get(Member.user_id == message.from_user.id)
    
    await message.answer((
        f"[{user.first_name}](tg://user?id={user.user_id}) ({user.role})\n"
        f"Warns: {user.warns}/{config.limit_of_warns}"),
        parse_mode="Markdown"
    )


@dp.message_handler(
    commands=["report2"],
    replied=True,
    chat_type=[types.ChatType.SUPERGROUP]
)
async def user_report(message: types.Message):
    args = message.text.split()

    if (len(args) != 2):
        await message.answer("/report (reason)")
        return

    reported_user = message.reply_to_message.from_user
    reporter_user = message.from_user
    reason = args[1]
    
    await bot.send_message(
        config.second_group_id,
        (
            "Complaint about: [{}](tg://user?id={})\n"
            "Complaint from: [{}](tg://user?id={})\n\n"
            "Note: {}\n"
            "{}"
        ).format(
            reported_user.first_name,
            reported_user.id,
            reporter_user.first_name,
            reporter_user.id,
            reason,
            message.reply_to_message.link("link message", as_html=False)
        ),
        parse_mode="Markdown",
    )
