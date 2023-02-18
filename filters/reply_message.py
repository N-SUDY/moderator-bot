from aiogram import types
from aiogram.filters import Filter


class MessageReplied(Filter):
    """Check if message replied"""

    def __init__(self, replied=True):
        self.replied = replied
    
    async def __call__(self, message: types.Message):
        if not message.reply_to_message:
            await message.reply("Is command must be reply")
            return False
        return True
