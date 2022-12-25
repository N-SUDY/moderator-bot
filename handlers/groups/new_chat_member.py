from load import dp, types
from database import Member

@dp.message_handler(content_types=["new_chat_members"])
async def welcome_message(message:types.Message):
    user = Member.get_or_none(Member.user_id == message.from_user.id)

        
    if (user):
        await message.answer(f"Hi, {user.first_name} again")

    if not (user):
        Member.create(
            user_id = message.from_user.id, 
            first_name = message.from_user.first_name,
            username = message.from_user.username,
        )

        await message.answer((
            f"Hi, **{user.first_name}**!\n"
            "Please, read [chat rules]({})"
            ).format(
                "https://nometa.xyz"
            ),parse_mode="Markdown")
    

    await message.delete()
