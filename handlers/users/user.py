from load import dp, bot, types
from database import Member, Restriction

import config

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from aiogram.fsm.state import State, StatesGroup

from aiogram import F
from aiogram.filters import Command
from filters import ChatTypeFilter


class ReportRestriction(StatesGroup):
    state1 = State()
    state2 = State()


@dp.message(
    Command("start", "help"),
    ChatTypeFilter("private")
)
async def start_command_private(message: types.Message):
    bot_description_menu = ReplyKeyboardBuilder()
    
    bot_description_menu.button(text="Check restrictions")
    bot_description_menu.button(text="About Us")

    await message.answer((
        f"Hi, **{message.from_user.first_name}**!\n"
        "My commands:\n"
        "\t\t/help /start - read this message."
    ), reply_markup=bot_description_menu.as_markup(resize_keyboard=True))


@dp.message(F.text == "About Us")
async def about_us(message: types.Message):
    await message.answer((
        "Moderator bot - an open source project for managing a Telegram group.\n\n"
        "Possibilities:\n"
        "1. Role system\n"
        "2. Simple commands such as !ban, !mute\n"
        "3. Convenient sticker/photo disabling with !stickers, !media\n"
        "4. Users can report admins.\n"
        "5. Admins can give warnings to users.\n"
        "\nRelease version: 2.5.2\n"
       "[Github](https://github.com/hok7z/moderator-bot)")
    )


@dp.message(F.text == "Check restrictions")
async def check_for_restrict(message: types.Message, state: FSMContext):
    await state.set_state(ReportRestriction.state1)
    user = Member.get(Member.user_id == message.from_user.id)
    restrictions = Restriction.select().where(Restriction.to_user == user)
    
    if (not restrictions):
        await message.answer("✅No restrictions.")
        return

    for restriction in restrictions:
        markup = InlineKeyboardBuilder()
        
        markup.button(
            text="✉️ Report restriction",
            callback_data=restriction.id
        )

        from_user = restriction.from_user
        to_user = restriction.to_user
        
        await message.answer((
            "Restriction #{}\n"
            "from user [{}](tg://user?id={})\n"
            "to user [{}](tg://user?id={})\n"
            "Note: {}\n"
            "{}\n"
        ).format(
            restriction.id,

            from_user.first_name,
            from_user.user_id,
            
            to_user.first_name,
            to_user.user_id,

            restriction.text,
            restriction.timestamp
        ), reply_markup=markup.as_markup())
    
    await state.set_state(ReportRestriction.state1)


@dp.callback_query(ReportRestriction.state1)
async def report_restriction(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    
    callback_data = call.data
    restriction_id = int(callback_data)

    cancel_markup = ReplyKeyboardBuilder()
    cancel_markup.button(text="❌ Cancel")

    await state.update_data(restriction_id=restriction_id)

    await call.message.answer(
        "Please,enter your report",
        reply_markup=cancel_markup.as_markup(resize_keyboard=True)
    )
    
    await state.set_state(ReportRestriction.state2)


@dp.message(ReportRestriction.state2)
async def get_message_report(message: types.Message, state: FSMContext):
    answer = message.text

    if not ("Cancel" in answer):
        data = await state.get_data()
        restriction_id = data.get("restriction_id")
        restriction = Restriction.get(id=restriction_id)

        from_user = restriction.from_user
        to_user = restriction.to_user
        
        restriction_timestamp = restriction.timestamp.strftime("%d.%m.%y at %H:%M")

        await bot.send_message(config.second_group_id, (
            "Report on restriction #{}\n"
            "Complaint from: [{}](tg://user?id={})\n"
            "Complaint about: [{}](tg://user?id={})\n"
            "Sent {}\n"
            "{}\n"
            "Message: {}"
        ).format(
            restriction_id,
            from_user.first_name,
            from_user.user_id,
            to_user.first_name,
            to_user.user_id,
            restriction.text,
            restriction_timestamp,
            answer,
        ))

        await message.answer(
            "Report restriction sended",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Operation cancaled",
            reply_markup=ReplyKeyboardRemove()
        )
    
    await state.clear()
