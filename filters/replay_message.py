from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class ReplayMessageFilter(BoundFilter):
    """Check if message replied"""
    key = 'replied'

    def __init__(self, replied):
        self.replied = replied

    async def check(self, message: types.Message):
        if message.reply_to_message is None:
            await message.reply("Is command must be reply")
            return False
        return True
