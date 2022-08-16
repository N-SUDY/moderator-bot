from load import bot, database, dp, types
from aiogram.types.chat_permissions import ChatPermissions

import config
import utils

from database.models import Member

import re

from dataclasses import dataclass

from database.models import MemberRoles

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
    user:Member | None
    arguments:list

async def getCommandArgs(message:types.Message) -> CommandArguments:
    """ Describe user data and arguments from message """
    
    """
    !command (@username/id) reason=None
    """

    arguments_list = message.text.split()[1:]
    
    is_reply = message.reply_to_message

    member = None
    arguments = []

    if (is_reply):
        member = database.search_single_member(Member.user_id,message.reply_to_message)
        arguments = arguments_list
    else:
        first_word = getArgument(arguments_list)
        if (first_word):
            if (first_word.isdigit()):
                member = database.search_single_member(Member.user_id,first_word)

            if (first_word[0] == "@") :
                member = database.search_single_member(Member.user_name,first_word)
            
            arguments = arguments_list[1:]
        else:
            arguments = arguments_list

        if (member is None) and (first_word):
            await message.answer(f"❌ User {first_word} not exist.")

    return CommandArguments(member,arguments)

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
    

def delete_substring_from_string(string:str,substring:str) -> str:
    string_list = string.split(substring)
    return "".join(string_list).lstrip()

# Filters:
# is_admin=True - Check admin permission, if user is admin, continue.
# replied=True  - If message is answer, continue.
# accessed_roles - list roles.

@dp.message_handler(commands=["ban"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN,MemberRoles.HELPER])
async def ban_user(message: types.Message):
    """
    !ban (@username/id) reason=None
    """
    command = await getCommandArgs(message)
    reason = getArgument(command.arguments)

    user = command.user
    admin = message.from_user

    # If can't descibe user data
    if (user is None):
        await message.answer((
            "Usage:!ban (@username|id) reason=None.\n"
            "Reply to a message or use with a username.")
        )
        return
    
    # Ban user and save (bool)
    status = await bot.kick_chat_member(chat_id=message.chat.id, user_id=user.user_id, until_date=None)
    
    if status:
        await message.answer(f"User [{user.first_name}](tg://user?id={user.user_id}) has been banned.",
            parse_mode="Markdown")
    
    # Delete user from database
    database.delete_user(user.user_id)
    
    # Open restrict
    database.create_restriction(admin.id, user.user_id, "ban", reason)


@dp.message_handler(commands=["unban"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN,MemberRoles.HELPER])
async def unban_user(message: types.Message):
    """
    !unban (@username/id) reason=None
    """
    command = await getCommandArgs(message)
    user = command.user

    # If can't descibe user data
    if (user is None):
        await message.answer((
            "Usage:!unban (@username|id) reason=None.\n"
            "Reply to a message or use with username/id.")
        )
        return
    
    # Unban user and set status (bool)
    status = await bot.unban_chat_member(chat_id=message.chat.id, user_id=user.user_id) 

    # add user to database
    database.register_user(user.user_id, user.first_name)

    if status:
        await message.answer(f"User [{user.first_name}](tg://user?id={user.user_id}) has been unbaned.",
            parse_mode="Markdown")


@dp.message_handler(commands=["kick"],commands_prefix="!",
    available_roles=[MemberRoles.HELPER,MemberRoles.ADMIN])
async def kick_user(message:types.Message):
    """
    !kick (@username/id) reason=None
    """
    
    command = await getCommandArgs(message)
    arguments = command.arguments
    
    user = command.user
    admin = message.from_user
    
    reason = getArgument(arguments)

    if (user is None):
        await message.answer((
            "Usage:!kick (@username|id) reason=None.\n"
            "Reply to a message or use with a username/id.")
        )
        return
    

    status1 = await bot.kick_chat_member(chat_id=message.chat.id, user_id=user.user_id, until_date=None)
    status2 = await bot.unban_chat_member(chat_id=message.chat.id, user_id=user.user_id)
    
    if (status1 and status2):
        await message.answer(f"User [{user.first_name}](tg://user?id={user.user_id}) has been kicked.",
                parse_mode="Markdown")
    
    database.create_restriction(admin.id,user.user_id,"kick",reason)


@dp.message_handler(commands=["mute"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN])
async def mute_user(message:types.Message):
    """
    !mute (@username/id) reason=None
    """ 
    
    command = await getCommandArgs(message)  
    arguments = command.arguments
    
    user = command.user
    admin = message.from_user

    if (user is None):
        await message.answer((
            "Usage:!mute (@username|id) [duration].\n"
            "Reply to a message or use with a username/id.")
        )
        return
    
    duration = re.findall(r"(\d+d|\d+h|\d+m|\d+s)",''.join(arguments))
    duration = " ".join(duration)
    reason = delete_substring_from_string(" ".join(arguments),duration)
    duration_timedelta = utils.parse_timedelta(duration)
    
    if not duration:
        await message.answer(f"Error: \"{duration}\" — неверный формат времени. Examles: 3ч, 5м, 4h30s.")
        return

    permissions = ChatPermissions(can_send_messages=False)

    status = await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user.user_id,
        until_date=duration_timedelta,
        permissions=permissions
    )

    if status:
        await message.answer(f"User **{user.first_name}** has been muted.",
            parse_mode="Markdown")

    database.create_restriction(user.user_id, admin.id, "mute", reason)


@dp.message_handler(commands=["umute"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN])
async def umute_user(message: types.Message):
    """
    !umute (@username/id) reason=None
    """
    # Get information
    command = await getCommandArgs(message)
    user = command.user

    # If can't  
    if (user is None):
        await message.answer((
            "Usage:!unmute (@username|id) reason=None.\n"
            "Reply to a message or use with a username/id.")
        )
        return 

    # Get chat permissions
    group_permissions = config.group_permissions

    # Set permissions
    permissions = ChatPermissions(
        can_send_messages=         group_permissions["can_send_messages"],
        can_send_media_messages=   group_permissions["can_send_media_messages"],
        can_send_polls=            group_permissions["can_send_polls"],
        can_send_other_messages=   group_permissions["can_send_other_messages"],
        can_add_web_page_previews= group_permissions["can_add_web_page_previews"],
        can_change_info=           group_permissions["can_change_info"],
        can_invite_users=          group_permissions["can_invite_users"],
        can_pin_messages=          group_permissions["can_pin_messages"]
    )

    # Restrict user and save
    status = await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user.user_id,
        permissions=permissions
    )

    if status:
        await message.answer(f"User [{user.first_name}](tg://user?id={user.user_id}) has been unmuted.",
            parse_mode="Markdown")        

@dp.message_handler(commands=["pin"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN,MemberRoles.HELPER])
async def pin_message(message:types.Message):
    await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)

@dp.message_handler(commands=["readonly","ro"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN])
async def readonly_mode(message:types.Message):
    """
    !ro/!readonly (@username/id)
    """
    check = checkArg(message.text)
    
    if (check is None):
        await message.answer("!ro on/off alias:disable,enable,start,stop.")
        return

    # Get chat permissions
    group_permissions = config.group_permissions

    # Set permissions
    if (check):
        chat_permissions = ChatPermissions( 
            can_send_messages=not check
        )
    else:
        chat_permissions = ChatPermissions(
            can_send_messages=group_permissions['can_send_messages'],
            can_send_media_messages=group_permissions["can_send_media_messages"],
            can_send_other_messages=group_permissions['can_send_other_messages'],
            can_send_polls=group_permissions['can_send_polls'],
            can_invite_users=group_permissions['can_invite_users'],
            can_change_info=group_permissions['can_change_info'],
            can_add_web_page_previews=group_permissions['can_add_web_page_previews'],
            can_pin_messages=group_permissions['can_pin_messages']
        )
    
    status = await bot.set_chat_permissions(chat_id=message.chat.id, permissions=chat_permissions) 
    
    if (status):
        await message.answer(f"readonly - {check}")


@dp.message_handler(commands=["media"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN,MemberRoles.HELPER])
async def media_content(message: types.Message):
    check = checkArg(message.text)
    
    if (check is None): 
        await message.answer("!media on/off alias:disable,enable,start,stop.")
        return

    # Get chat permissions
    group_permissions = config.group_permissions
    
    # Set permissions
    chat_permissions = ChatPermissions(
        can_send_messages=group_permissions['can_send_messages'],
        can_send_media_messages=check,
        can_send_other_messages=group_permissions['can_send_other_messages'],
        can_send_polls=group_permissions['can_send_polls'],
        can_invite_users=group_permissions['can_invite_users'],
        can_change_info=group_permissions['can_change_info'],
        can_add_web_page_previews=group_permissions['can_add_web_page_previews'],
        can_pin_messages=group_permissions['can_pin_messages']
    )

    # Set chat pemissions and save results
    status = await bot.set_chat_permissions(chat_id=message.chat.id, permissions=chat_permissions)
    
    if status:
        await message.answer(f"media - {check}.")        


@dp.message_handler(commands=["stickers"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN,MemberRoles.HELPER])
async def send_stickers(message: types.Message):
    # Get arguments
    check = checkArg(message.text)
    
    if (check is None):
        await message.answer("!stickers on/off alias:disable,enable,start,stop")
        return
    
    # Get chat permissions
    group_permissions = config.group_permissions

    # Set permissions.
    chat_permissions = ChatPermissions(
        can_send_messages=group_permissions['can_send_messages'],
        can_send_media_messages=group_permissions['can_send_media_messages'],
        can_send_other_messages=check,
        can_send_polls=group_permissions['can_send_polls'],
        can_invite_users=group_permissions['can_invite_users'],
        can_change_info=group_permissions['can_change_info'],
        can_add_web_page_previews=group_permissions['can_add_web_page_previews'],
        can_pin_messages=group_permissions['can_pin_messages']
    )

    # Start and save to satus (bool)
    status = await bot.set_chat_permissions(chat_id=message.chat.id, permissions=chat_permissions)
    
    if status:
        await message.answer(f"stickes - {check}.")


@dp.message_handler(commands=["w","warn"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN,MemberRoles.HELPER])
async def warn_user(message: types.Message):
    # Get information
    command = await getCommandArgs(message)
    reason = getArgument(command.arguments) 

    user = command.user
    admin = message.from_user
    
    if (user is None):
        await message.answer((
            "Usage:!warn (@username/id) reason=None.\n"
            "Reply to a message or use with username/id.")
        )
        return

    # Add warning
    database.change_reports(user.user_id, delete=True)

    await message.answer(f"User [{user.first_name}](tg://user?id={user.user_id}) has gotten a warning.",
        parse_mode="Markdown")
    
    database.create_restriction(user.user_id, admin.id, "warn", reason)


@dp.message_handler(commands=["reload"],commands_prefix="!",available_roles=[MemberRoles.ADMIN,MemberRoles.HELPER])
async def reload(message:types.Message):
    await utils.check_user_data()
    
    group = await bot.get_chat(message.chat.id)
    group_permissions = dict(group["permissions"])
     
    for permission in group_permissions.keys():
        config.group_permissions[permission] = group_permissions[permission]

    await message.answer(f"✅ The synchronization was successful.")


@dp.message_handler(commands=["set_role"],commands_prefix="!",
    available_roles=[MemberRoles.ADMIN])
async def set_role(message:types.Message):
    command = await getCommandArgs(message)
    new_role = getArgument(command.arguments)

    user = command.user
    admin = database.search_single_member(Member.user_id,message.from_user)
    
    if (user is None) or (new_role is None):
        await message.answer((
            "!srole (@username|id) role(owner,admin,helper,member).\n"
            "Reply to a message or use with username."
        ))
        return

    if not (new_role in [member.value for member in MemberRoles]):
        await message.answer(f"Role {new_role} not exists.")
        return
    
    if (admin.user_id == user.user_id):
        await message.answer("❌ You can't set role yourself.")
        return

    database.update_member_data(user.user_id,[Member.role],[new_role])
    
    await message.answer(f"{new_role.capitalize()} role set for [{user.first_name}](tg://user?id={user.user_id}).",parse_mode="Markdown")
