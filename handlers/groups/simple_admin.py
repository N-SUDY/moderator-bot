from load import bot, dp, types
from aiogram.types.chat_permissions import ChatPermissions

import config

from database import Restriction
from database import MemberRoles

from utils import get_command_args, get_argument, parse_timedelta_from_message


@dp.message_handler(
    commands=["ban", "sban"],
    commands_prefix="!",
    available_roles=[MemberRoles.HELPER, MemberRoles.ADMIN]
)
async def ban_user(message: types.Message):
    command = await get_command_args(message)
    
    to_user = command.to_user
    from_user = command.from_user

    if (not to_user) or (not from_user):
        await message.answer((
            "Usage: !ban (@username|id) reason=None\n"
            "Reply to a message or use with a username")
        )
        return
    
    status = await bot.kick_chat_member(
        chat_id=message.chat.id,
        user_id=to_user.user_id,
        until_date=None
    )
    
    if status and (not command.is_silent):
        await message.answer((
            f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has banned "
            f"[{to_user.first_name}](tg://user?id={to_user.user_id})"
        ), parse_mode="Markdown")
     
    Restriction.create(
        from_user=from_user,
        to_user=to_user,
        text=message.text,
        message_id=message.message_id
    )


@dp.message_handler(
    commands=["unban", "sunban"],
    commands_prefix="!",
    available_roles=[MemberRoles.HELPER, MemberRoles.ADMIN]
)
async def unban_user(message: types.Message):
    command = await get_command_args(message)
    
    to_user = command.to_user
    from_user = command.from_user

    if (not to_user) or (not from_user):
        await message.answer((
            "Usage: !unban (@username|id) reason=None\n"
            "Reply to a message or use with username/id")
        )
        return
    
    status = await bot.unban_chat_member(chat_id=message.chat.id, user_id=to_user.user_id) 

    if status and (not command.is_silent):
        await message.answer((
            f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has unbanned "
            f"[{to_user.first_name}](tg://user?id={to_user.user_id})"
        ), parse_mode="Markdown")

    Restriction.create(
        from_user=from_user,
        to_user=to_user,
        text=message.text,
        message_id=message.message_id
    )


@dp.message_handler(
    commands=["info"],
    commands_prefix="!",
    available_roles=[MemberRoles.HELPER, MemberRoles.ADMIN]
)
async def info_user(message: types.Message):
    command = await get_command_args(message)
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


@dp.message_handler(
    commands=["kick", "skick"],
    commands_prefix="!",
    available_roles=[MemberRoles.HELPER, MemberRoles.ADMIN]
)
async def kick_user(message: types.Message):
    command = await get_command_args(message)

    to_user = command.to_user
    from_user = command.from_user
    
    if (not to_user) or (not from_user):
        await message.answer((
            "Usage: !kick (@username|id) reason=None\n"
            "Reply to a message or use with a username/id")
        )
        return
    

    status1 = await bot.kick_chat_member(
        chat_id=message.chat.id,
        user_id=to_user.user_id,
        until_date=None
    )
    
    status2 = await bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=to_user.user_id
    )
    
    if (not status1 and status2) and (not command.is_silent):
        await message.answer((
            f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has kicked "
            f"[{to_user.first_name}](tg://user?id={to_user.user_id})"
        ), parse_mode="Markdown")

    Restriction.create(
        from_user=from_user,
        to_user=to_user,
        text=message.text,
        message_id=message.message_id
    )


@dp.message_handler(
    commands=["mute", "smute"],
    commands_prefix="!",
    available_roles=[MemberRoles.ADMIN]
)
async def mute_user(message: types.Message):
    command = await get_command_args(message)

    to_user = command.to_user
    from_user = command.from_user

    duration = parse_timedelta_from_message(message)
    
    if (not to_user) or (not from_user):
        await message.answer((
            "Usage:!mute (@username|id) (duration)\n"
            "Reply to a message or use with a username/id")
        )
        return

    permissions = ChatPermissions(can_send_messages=False)

    status = await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=to_user.user_id,
        until_date=duration,
        permissions=permissions
    )
    
    if status and (not command.is_silent):
        await message.answer((
            f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has muted "
            f"[{to_user.first_name}](tg://user?id={to_user.user_id})"
        ), parse_mode="Markdown")
    
    Restriction.create(
        from_user=from_user,
        to_user=to_user,
        text=message.text,
        message_id=message.message_id
    )


@dp.message_handler(
    commands=["unmute", "sunmute"],
    commands_prefix="!",
    available_roles=[MemberRoles.ADMIN]
)
async def umute_user(message: types.Message):
    # Get information
    command = await get_command_args(message)
    
    to_user = command.to_user
    from_user = command.from_user

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
        can_send_messages=group_permissions["can_send_messages"],
        can_send_media_messages=group_permissions["can_send_media_messages"],
        can_send_polls=group_permissions["can_send_polls"],
        can_send_other_messages=group_permissions["can_send_other_messages"],
        can_add_web_page_previews=group_permissions["can_add_web_page_previews"],
        can_change_info=group_permissions["can_change_info"],
        can_invite_users=group_permissions["can_invite_users"],
        can_pin_messages=group_permissions["can_pin_messages"]
    )

    # Restrict user and save
    status = await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=to_user.user_id,
        permissions=permissions
    )

    if status and (not command.is_silent):
        await message.answer((
            f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has unmuted "
            f"[{to_user.first_name}](tg://user?id={to_user.user_id})"
        ), parse_mode="Markdown")


@dp.message_handler(
    commands=["pin"],
    commands_prefix="!",
    available_roles=[MemberRoles.HELPER, MemberRoles.ADMIN]
)
async def pin_message(message: types.Message):
    await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)


@dp.message_handler(
    commands=["readonly", "ro"],
    commands_prefix="!",
    available_roles=[MemberRoles.ADMIN]
)
async def readonly_mode(message: types.Message):
    group_permissions = config.group_permissions
    status = config.group_permissions['can_send_messages']
    
    if (status):
        await message.answer("🔕 Readonly mode enabled!")
        chat_permissions = ChatPermissions(
            can_send_messages=not status
        )
    else:
        await message.answer("🔔 Readonly mode disabled!")
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

    config.group_permissions["can_send_messages"] = not status
    await bot.set_chat_permissions(
        chat_id=message.chat.id,
        permissions=chat_permissions
    )


@dp.message_handler(
    commands=["warn", "w"],
    commands_prefix="!",
    available_roles=[MemberRoles.HELPER, MemberRoles.ADMIN]
)
async def warn_user(message: types.Message):
    # Get information
    command = await get_command_args(message)
    
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
    
    await message.answer((
        f"[{from_user.first_name}](tg://user?id={from_user.user_id}) has warned "
        f"[{to_user.first_name}](tg://user?id={to_user.user_id})"
    ), parse_mode="Markdown")

    if (to_user.warns == config.limit_of_warns):
        await message.answer((
            f"[{from_user.first_name}](tg://user?id={from_user.user_id}) "
            f"has banned {config.limit_of_warns}/{config.limit_of_warns} ⚠️ "
        ), parse_mode="Markdown")

        await bot.kick_chat_member(
            chat_id=message.chat.id,
            user_id=to_user.user_id,
            until_date=None
        )
   
    Restriction.create(
        from_user=from_user,
        to_user=to_user,
        text=message.text,
        message_id=message.message_id
    )


@dp.message_handler(
    commands=["reload"],
    commands_prefix="!"
)
async def reload(message: types.Message):
    from utils import reload_users_data
    await reload_users_data()
    
    await message.answer("Reloaded!")


@dp.message_handler(
    commands=["setrole"],
    commands_prefix="!",
    available_roles=[MemberRoles.ADMIN]
)
async def set_role(message: types.Message):
    command = await get_command_args(message)
    new_role = get_argument(command.arguments)

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
    
    await message.answer((
        f"{new_role.capitalize()} role set for "
        f"[{to_user.first_name}](tg://user?id={to_user.user_id})"
    ), parse_mode="Markdown")
