from dataclasses import dataclass
from database import Member
from aiogram import types

import re

def getArgument(arguments:list,index:int=0) -> str | None:
    """ Get element from a list.If element not exist return None """
    if not (arguments):
        return None
    
    if (len(arguments) > index):
        return arguments[index]
    else:
        return None

@dataclass
class CommandArguments:
    to_user:Member | None
    from_user:Member | None
    arguments:list

async def getCommandArgs(message: types.Message) -> CommandArguments:
    """
        Describe user data and arguments from message
        !command (username|id) ...
    """
    

    arguments = message.text.split()[1:]
    to_user = None
    from_user = Member.search(Member.user_id, message.from_user.id)
    
    # If message replied
    if (message.reply_to_message):
        to_user = Member.search(Member.user_id, message.reply_to_message)
    else:
        user_data = getArgument(arguments)
        
        if (user_data):
            if (user_data.isdigit()):
                to_user = Member.search(Member.user_id, user_data)
            
            if (user_data[0] == "@"):
                to_user = Member.search(Member.username, user_data)

        if (arguments) and (not to_user):
            await message.answer(f"❌ User {to_user} not exist.")
        
        arguments = arguments[1:]

    return CommandArguments(to_user, from_user, arguments)


def delete_substring_from_string(string:str,substring:str) -> str:
    string_list = string.split(substring)
    return "".join(string_list).lstrip()

def parse_duration(message) -> str:
    duration = re.findall(r"(\d+d|\d+h|\d+m|\d+s)",''.join(message))
    duration = " ".join(duration)
    return duration

def checkArg(message:str) -> bool | None:
    """ Check if first argument in ["enable","on","true"] then return true """
    if (not message):
        return None
    
    argument = message.split()
    argument = getArgument(message.split(),1)
    
    if (argument is None):
        return None

    on  = ['enable','on','true']
    off = ['disable','off','false']
    
    if (argument in on):
        return True
    if (argument in off):
        return False
