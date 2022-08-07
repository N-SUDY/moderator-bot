from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def report_button(text,callback_data):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text,callback_data=callback_data)
    markup.insert(button)
    return markup
