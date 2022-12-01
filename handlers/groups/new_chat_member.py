from load import dp, types
from database import Member

@dp.message_handler(content_types=["new_chat_members"])
async def welcome_message(message:types.Message):
    user = Member.get_or_none(Member.user_id == message.from_user.id)

        
    if (user):
        await message.answer("Спасибо что вы с нами.")

    if not (user):
        Member.create(
            user_id = message.from_user.id, 
            first_name = message.from_user.first_name,
            username = message.from_user.username,
        )

        # TODO: translate it    
        await message.answer((
            f"Привет,{user.first_name}\n"
            "Просим ознакомится с [правилами](https://telegra.ph/Pravila-CHata-Open-Source-05-29)\n"
            "Советы на 'хороший тон':\n"
            "\t\t1.Формулируй свою мысль в 1-2 предложения\n"
            "\t\t1.Не задавай [мета](nometa.xyz) вопросы\n"),
        parse_mode="Markdown")
    

    await message.delete()
