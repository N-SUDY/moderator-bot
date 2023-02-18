from aiogram import types
from aiogram.filters import Filter
from database import Member, MemberRoles


class AvailableRoles(Filter):
    """Filter accessed roles"""
    
    def __init__(self, *args):
        self.avaible_roles: list[MemberRoles] = args

    async def __call__(self, message: types.Message) -> bool:
        member = Member.get(Member.user_id == message.from_user.id)
        
        if (member.role == "owner"):
            return True
         
        status = member.role in [role.value for role in self.avaible_roles]
        if (not status):
            await message.answer("Command not avaible")

        return status
