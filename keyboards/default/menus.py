from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


bot_description_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[
        KeyboardButton("Check restrictions"),
        KeyboardButton("About Us"),
    ]]
)


cancel_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[
        KeyboardButton("❌Cancel")
    ]]
)
