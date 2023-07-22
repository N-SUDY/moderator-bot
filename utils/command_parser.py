from typing import Optional
from dataclasses import dataclass
from database import Member

from load import types


@dataclass
class CommandArguments:
    to_user: Optional[Member]
    from_user: Optional[Member]
    arguments: list
    is_silent: bool


def get_argument(arguments: list, index: int = 0) -> Optional[str]:
    """ Get element from a list.If element not exist return None """
    if not (arguments):
        return None
    
    if (len(arguments) > index):
        return arguments[index]
    else:
        return None


async def get_command_args(message: types.Message) -> CommandArguments:
    """Describe user data and arguments from message"""
    
    silent = message.text.split()[0] == "s"
    
    arguments = message.text.split()[1:]
    to_user = None
    from_user = Member.get(Member.user_id == message.from_user.id)
    
    # If message replied
    if (message.reply_to_message):
        to_user = Member.get_or_none(Member.user_id == message.reply_to_message)
    else:
        user_data = get_argument(arguments)
        
        if (user_data):
            if (user_data.isdigit()):
                to_user = Member.get(Member.user_id == user_data)
            if (user_data[0] == "@"):
                to_user = Member.get(Member.username == user_data)
        
        arguments = arguments[1:]

    return CommandArguments(to_user, from_user, arguments, silent)
