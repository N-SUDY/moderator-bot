from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

# from config import roles
from database.database import Member

class IsAdminFilter(BoundFilter):
    """Check admin permission on hadler"""
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        result = member.is_chat_admin()
        if not result:
            await message.reply("🔒This command can only be used by an admin!")
        return result

class UserHasRights(BoundFilter):
    """Check command in user rights"""
   
    key = 'hasRights'
   
    def __init__(self,hasRights):
        self.hasRights = hasRights

    async def check(self,message:types.Message):
        import config
        from load import database
        
        roles = config.roles["roles"]

        command = message.text.split()[0].lstrip("!")

        user = database.search_single_member(Member.user_id,message.from_user.id)
       
        # If data not exists,return False
        if (user is None):
            return False
       
        # If role not exist,return False.
        if not (user.role in roles.keys()):
            return False
        
        can_run_it = roles[user.role][command]
        
        replied = message.reply_to_message
        
        if (replied):
            if (replied.from_user.id == message.from_user.id):
                await message.answer("❌ You can't ")
                return False

            if (str(replied.from_user.id) == config.token.split(":")[0]):
                await message.answer("You can't restrict bot.")
                return False
        
        if not (can_run_it):
            await message.answer("You can't use this command.")
            return False

        return roles[user.role][command]

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
