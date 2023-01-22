from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


report_callback = CallbackData("report_restriction", "restriction_id")


def inline_button(text, callback_data):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text, callback_data=callback_data)
    markup.insert(button)
    return markup
