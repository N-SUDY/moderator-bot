from load import bot, dp, types
from aiogram.types.chat_permissions import ChatPermissions

import config
import utils


from database import Member, Restriction
from database import MemberRoles

from utils import getCommandArgs, getArgument, checkArg, parse_duration, delete_substring_from_string


#  Filters
#  is_admin=True - Check admin permission, if user is admin, continue.
#  replied=True  - If message is answer, continue.
#  accessed_roles - list roles.

@dp.message_handler(commands=["ban"],commands_prefix="!",available_roles=[MemberRoles.HELPER,MemberRoles.ADMIN])
async def ban_user(message: types.Message):
    command = await getCommandArgs(message)
    reason = getArgument(command.arguments)

    to_user = command.to_user
    from_user = command.from_user

    # If can't descibe user data
    if (not to_user) or (not from_user):
        await message.answer((
            "Usage: !ban (@username|id) reason=None\n"
            "Reply to a message or use with a username")
        )
        return
    
    # Ban user and save (bool)
    status = await bot.kick_chat_member(chat_id=message.chat.id, user_id=to_user.user_id, until_date=None)
    
    if status:
        await message.answer(f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has banned [{to_user.first_name}](tg://user?id={to_user.user_id})",parse_mode="Markdown")
     
     
    # Open restrict
    Restriction.create(
        from_user=from_user,
        to_user=to_user,
        action="Ban user",
        reason=reason,
    )

@dp.message_handler(commands=["unban"],commands_prefix="!",available_roles=[MemberRoles.HELPER,MemberRoles.ADMIN])
async def unban_user(message: types.Message):
    command = await getCommandArgs(message)
    
    to_user = command.to_user
    from_user = command.from_user

    # If can't descibe user data
    if (not to_user) or (not from_user):
        await message.answer((
            "Usage: !unban (@username|id) reason=None\n"
            "Reply to a message or use with username/id")
        )
        return
    
    # Unban user and set status (bool)
    status = await bot.unban_chat_member(chat_id=message.chat.id, user_id=to_user.user_id) 
    

    if status:
        await message.answer(f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has unbanned [{to_user.first_name}](tg://user?id={to_user.user_id})",parse_mode="Markdown")
    
    Member.create(
        user_id = to_user.user_id,
        first_name = to_user.first_name,
        username = to_user.username
    )

@dp.message_handler(commands=["info"],commands_prefix="!",available_roles=[MemberRoles.HELPER,MemberRoles.ADMIN])
async def info_user(message: types.Message):
    command = await getCommandArgs(message) 
    
    to_user = command.to_user 
    
    if (not to_user):
        await message.answer((
            "Usage: !info (@username|id)\n"
            "Reply to a message or use with username/id")
        )
        return

    await message.answer((
        f"[{to_user.first_name}](tg://user?id={to_user.user_id}) ({to_user.role})\n"
        f"Warns: {to_user.warns}/{config.limit_of_warns}"),
        parse_mode="Markdown"
    )

@dp.message_handler(commands=["kick"],commands_prefix="!",available_roles=[MemberRoles.HELPER,MemberRoles.ADMIN])
async def kick_user(message:types.Message):
    command = await getCommandArgs(message)
    arguments = command.arguments
    
    to_user = command.to_user
    from_user = command.from_user
    
    reason = getArgument(arguments)

    if (not to_user) or (not from_user):
        await message.answer((
            "Usage: !kick (@username|id) reason=None\n"
            "Reply to a message or use with a username/id")
        )
        return
    

    status1 = await bot.kick_chat_member(chat_id=message.chat.id, user_id=to_user.user_id, until_date=None)
    status2 = await bot.unban_chat_member(chat_id=message.chat.id, user_id=to_user.user_id)
    
    if (not status1 and status2):
        await message.answer(f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has kicked [{to_user.first_name}](tg://user?id={to_user.user_id})",parse_mode="Markdown")
    
    
    Restriction.create(
        from_user=from_user,
        to_user=to_user,
        action="Kick user",
        reason=reason,
    )


@dp.message_handler(commands=["mute"],commands_prefix="!",available_roles=[MemberRoles.ADMIN])
async def mute_user(message:types.Message):
    command = await getCommandArgs(message)  
    arguments = command.arguments
    
    to_user = command.to_user
    from_user = command.from_user

    if (not to_user) or (not from_user):
        await message.answer((
            "Usage:!mute (@username|id) (duration)\n"
            "Reply to a message or use with a username/id")
        )
        return
     
    duration_string = parse_duration(arguments) 
    duration = None
    reason = None

    if (duration_string):
        duration = utils.parse_timedelta(duration_string)

        if (not duration):
            await message.answer(f"Error: \"{duration}\" — неверный формат времени. Examles: 3ч, 5м, 4h30s.")
            return
        
        reason = delete_substring_from_string(" ".join(arguments),duration_string)    
        
    if (not duration_string):
        duration_string = "forever"
        
        if (arguments):
            reason = " ".join(arguments)

    permissions = ChatPermissions(can_send_messages=False)

    status = await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=to_user.user_id,
        until_date=duration,
        permissions=permissions
    )
    
    if status:
        await message.answer(f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has muted [{to_user.first_name}](tg://user?id={to_user.user_id}) for {duration_string}",parse_mode="Markdown")
    

    Restriction.create(
        from_user=from_user,
        to_user=to_user,
        action="Mute user",
        reason=reason,
    )


@dp.message_handler(commands=["unmute"],commands_prefix="!",available_roles=[MemberRoles.ADMIN])
async def umute_user(message: types.Message):
    # Get information
    command = await getCommandArgs(message)
    
    to_user = command.to_user
    from_user = command.from_user

    # If can't  
    if (not to_user) or (not from_user):
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
        user_id=to_user.user_id,
        permissions=permissions
    )

    if status:
        await message.answer(f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has unmuted [{to_user.first_name}](tg://user?id={to_user.user_id})",parse_mode="Markdown")

@dp.message_handler(commands=["pin"],commands_prefix="!",available_roles=[MemberRoles.HELPER,MemberRoles.ADMIN])
async def pin_message(message:types.Message):
    await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)

@dp.message_handler(commands=["readonly","ro"],commands_prefix="!",available_roles=[MemberRoles.ADMIN])
async def readonly_mode(message:types.Message):
    check = checkArg(message.text)
    
    if (not check):
        await message.answer("Usage:!ro on,enable,start/off,disable,off\n")
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


@dp.message_handler(commands=["media"],commands_prefix="!",available_roles=[MemberRoles.ADMIN,MemberRoles.HELPER])
async def media_content(message: types.Message):
    check = checkArg(message.text)
    
    if (not check): 
        await message.answer("Usage: !media on,enable,start/off,disable,off")
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
        await message.answer(f"media - {check}")        


@dp.message_handler(commands=["stickers"],commands_prefix="!",available_roles=[MemberRoles.ADMIN,MemberRoles.HELPER])
async def send_stickers(message: types.Message):
    # Get arguments
    check = checkArg(message.text)
    
    if (not check):
        await message.answer("Usage: !stickers on,enable,start/off,disable,off")
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
        await message.answer(f"stickes - {check}")


@dp.message_handler(commands=["warn","w"],commands_prefix="!",available_roles=[MemberRoles.HELPER,MemberRoles.ADMIN])
async def warn_user(message: types.Message):
    # Get information
    command = await getCommandArgs(message)
    reason = getArgument(command.arguments) 
    
    to_user = command.to_user
    from_user = command.from_user

    if (not to_user) or (not from_user):
        await message.answer((
            "Usage: !warn (@username|id) reason=None\n"
            "Reply to a message or use with username/id")
        )
        return

    to_user.warns += 1
    to_user.save()

    await message.answer(f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has warned [{to_user.first_name}](tg://user?id={to_user.user_id}) ({to_user.warns}/{config.limit_of_warns})",parse_mode="Markdown")
    

    if (to_user.warns == config.limit_of_warns):
        await message.answer(f"[{to_user.first_name}](tg://user?id={to_user.user_id}) has been banned!",parse_mode="Markdown")
        await bot.kick_chat_member(chat_id=message.chat.id, user_id=to_user.user_id, until_date=None)

    Restriction.create(
        to_user=to_user,
        from_user=from_user,
        action="Warn user",
        reason=reason,
    )


@dp.message_handler(commands=["reload"],commands_prefix="!")
async def reload(message:types.Message):
    from load import tgc

    if (not Member.search(Member.role,"owner")):
        Member.create(
            user_id = message.from_user.id,
            first_name = message.from_user.first_name,
            username = message.from_user.username,
            role="owner",
        )
    # TODO: do this every 1 hours    
    members = await tgc.members_list(config.group_id)
    
    for member in members:
        user = Member.search(Member.user_id,member["id"])
        
        if (not user):
            Member.create(
                user_id=member["id"],
                first_name=member["first_name"],
                username=member["username"],
            )
        else:
            user.first_name = member["first_name"]
            user.username = member["username"] 
            user.save()

    
    group = await bot.get_chat(message.chat.id)
    group_permissions = dict(group["permissions"])
     
    for permission in group_permissions.keys():
        config.group_permissions[permission] = group_permissions[permission]

    await message.answer("Reloaded!")


@dp.message_handler(commands=["setrole"],commands_prefix="!",available_roles=[MemberRoles.ADMIN])
async def set_role(message:types.Message):
    command = await getCommandArgs(message)
    new_role = getArgument(command.arguments)

    to_user = command.to_user
    from_user = command.from_user
    
    if (not to_user) or (not from_user) or (not new_role):
        await message.answer((
            "!setrole (@username|id) role(owner,admin,helper,member).\n"
            "Reply to a message or use with username."
        ))
        return

    if not (new_role in [member.value for member in MemberRoles]):
        await message.answer(f"Role {new_role} not exists")
        return
    
    if (from_user.user_id == to_user.user_id):
        await message.answer("❌ You can't set role yourself")
        return
    
    to_user.role = new_role
    to_user.save()

    await message.answer(f"{new_role.capitalize()} role set for [{to_user.first_name}](tg://user?id={to_user.user_id})",
        parse_mode="Markdown")
