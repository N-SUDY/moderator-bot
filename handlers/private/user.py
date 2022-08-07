from load import dp,types,database,bot
from database.models import Member

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
        "Hello,**{message.from_user.first_name}**!\n"
        "\t\tMy commands:\n"
        "\t\t/help , /start - read this message.")
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
    user = message.from_user
    restrictions = database.search_user_restriction(user_id=user.id)

    if (restrictions is None):
        await message.answer("✅No restrictions.")
        return

    for restriction in restrictions:
        callback = report_callback.new(user_id=message.from_user.id)
        markup = report_button("✉️ Report restriction",callback)

        await message.answer(f"Restriction\n{restriction.operation}\nReason:{restriction.reason}\nDate:{restriction.date}",reply_markup=markup)
        
    await States.state1.set() 

@dp.callback_query_handler(text_contains="report_restriction",state=States.state1)
async def report_restriction(call:CallbackQuery,state:FSMContext):
    await call.answer(cache_time=60)
    
    # callback_data  = call.data
    # restriction_id = callback_data.split(":")[1]
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = KeyboardButton("❌ Cancel")
    markup.add(cancel)

    await state.update_data(restriction_id=restriction_id)

    await call.message.answer("Please,enter your report.",reply_markup=markup)

@dp.message_handler(state=States.state2)
async def get_message_report(message: types.Message,state:FSMContext):
    answer = message.text
    
    if not ("Cancel" in answer):
        
        restriction = database.search_user_restriction(message.from_user.id)

        if (restriction is None):
            return

        #from_admin = restriction.from_admin
        #to_user    = restriction.to_user
        
        reason = restriction.reason
        if (not reason):
            reason = "No reason"

        await bot.send_message(config.telegram_log_chat_id,(
            f"Report on restriction #{restriction_id}\n"
            f"From admin:[{from_admin.first_name}](tg://user?id={from_admin.id})\n"
            f"To user:[{from_admin.first_name}](tg://user?id={to_user.id})\n"
            f"Reason:{reason}\n"
            f"Message:{answer}"
        ),parse_mode="Markdown")
        
        await message.answer("Report restriction sended",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Operation cancaled",reply_markup=ReplyKeyboardRemove())
    
    await state.finish()
