from load import dp, types, bot
from database import Member, Restriction

from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

import config
from keyboards.default import menu

from aiogram.types import CallbackQuery 
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher.storage import FSMContext
from states.report_message import States

from keyboards.inline.report_button import report_button
from keyboards.inline.callback_data import report_callback

@dp.message_handler(commands=["start","help"],chat_type=[types.ChatType.PRIVATE])
async def start_command_private(message:types.Message):
    await message.answer((
        f"Hi, **{message.from_user.first_name}**!\n"
        "My commands:\n"
        "\t\t/help /start - read this message.")
        ,parse_mode="Markdown",reply_markup=menu
    )

# Keyboard 
@dp.message_handler(Text(equals=["About Us"]))
async def about_us(message:types.Message):
    await message.answer((
        "Moderator bot - an open source project for managing a Telegram group.\n\n"
        "Possibilities:\n"
        "1. Role system\n"
        "2. Simple commands such as !ban, !mute\n"
        "3. Convenient sticker/photo disabling with !stickers, !media\n"
        "4. Users can report admins.\n"
        "5. Admins can give warnings to users.\n"
        "\nRelease version:2.5.2\n"
       "[Github](https://github.com/hok7z/moderator-bot)"),
       parse_mode="Markdown"
    )


@dp.message_handler(Text(equals=["Check restrictions"]),state=None)
async def check_for_restrict(message:types.Message):
    user = Member.get(Member.user_id == message.from_user.id)
    restrictions = Restriction.select().where(Restriction.to_user == user)

    if (not restrictions):
        await message.answer("✅No restrictions.")
        return

    for restriction in restrictions:
        callback = report_callback.new(restriction_id=restriction.id)
        markup = report_button("✉️ Report restriction",callback)
        
        from_user  = restriction.from_user
        to_user    = restriction.to_user
        
        await message.answer(
            (
                f"Restriction #{restriction.id}\n"
                f"from user: [{from_user.first_name}](tg://user?id={from_user.user_id})\n"
                f"to user: [{from_user.first_name}](tg://user?id={to_user.user_id})\n"
                f"{restriction.text}\n"
                f"{restriction.timestamp}\n"
            ),parse_mode="Markdown",
            reply_markup=markup
        )

    await States.state1.set() 

@dp.callback_query_handler(text_contains="report_restriction",state=States.state1)
async def report_restriction(call:CallbackQuery, state:FSMContext):
    await call.answer(cache_time=60)
    
    callback_data  = call.data
    restriction_id = callback_data.split(":")[1]

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = KeyboardButton("❌ Cancel")
    markup.add(cancel)

    await state.update_data(restriction_id=restriction_id)

    await call.message.answer("Please,enter your report.",reply_markup=markup)
    
    await States.next()

@dp.message_handler(state=States.state2)
async def get_message_report(message:types.Message, state:FSMContext):
    answer = message.text

    if not ("Cancel" in answer):
        data = await state.get_data()
        restriction_id = data.get("restriction_id") 
        restriction = Restriction.get(id=restriction_id)

        from_user  = restriction.from_user
        to_user    = restriction.to_user
        
        await bot.send_message(config.second_group_id,
            (
                "Report on restriction #{}\n"
                "from user: [{}](tg://user?id={})\n"
                "to user: [{}](tg://user?id={})\n"
                "{}\n"
                "{}\n"
                "Message:{}"
            ).format(
                restriction_id,
                from_user.first_name,
                from_user.user_id,
                to_user.first_name,
                to_user.user_id,
                restriction.text,
                restriction.timestamp,
                answer,
            )
            ,parse_mode="Markdown"
        )

        await message.answer("Report restriction sended",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Operation cancaled",reply_markup=ReplyKeyboardRemove())
    
    await state.finish()
