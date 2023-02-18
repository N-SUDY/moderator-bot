from load import bot, dp, types
from aiogram import Bot
import config
from aiogram.filters import Command

from filters import MessageReplied
from filters import ChatTypeFilter

from database import Member

from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, JOIN_TRANSITION, ChatMemberUpdated


@dp.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION)
)
async def welcome_message(event: ChatMemberUpdated, _bot: Bot):
    user = Member.get_or_none(Member.user_id == event.from_user.id)

    if (user):
        await _bot.send_message(
            chat_id=event.chat.id,
            text=f"Hi, {user.first_name} again"
        )

    if not (user):
        Member.create(
            user_id=event.from_user.id,
            first_name=event.from_user.first_name,
            username=event.from_user.username,
        )
            
        await _bot.send_message(
            chat_id=event.chat.id,
            text=f"Hi, [{user.first_name}](tg://user?id={user.id})!\n"
            "Please, read [chat rules](https://nometa.xyz)"
        )


@dp.message(
    Command("start", "help"),
    ChatTypeFilter("supergroup")
)
async def start_command_group(message: types.Message):
    await message.answer((
        f"Hi, [{message.from_user.first_name}](tg://user?id={message.from_user.id})!\n"
        "My commands:\n"
        "    /help , /start - read the message\n"
        "    /me   , /bio   - member information (if member group)")
    )


@dp.message(
    Command("leave"),
    ChatTypeFilter("supergroup")
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
        ))
    
    Member.delete().where(Member.user_id == user.id).execute()


@dp.message(
    Command("bio", "me"),
    ChatTypeFilter("supergroup")
)
async def get_information(message: types.Message):
    user = Member.get(Member.user_id == message.from_user.id)
    
    await message.answer((
        f"[{user.first_name}](tg://user?id={user.user_id}) ({user.role})\n"
        f"Warns: {user.warns}/{config.limit_of_warns}"
    ))


@dp.message(
    Command("report"),
    MessageReplied(),
    ChatTypeFilter("supergroup")
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
        )
    )
