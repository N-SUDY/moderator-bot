async def reload_users_data():
    import config
    from database import Member
    from load import tgc, bot

    members = await tgc.members_list(config.group_id)

    for member in members:
        user = Member.get_or_none(Member.user_id == member["id"])
        
        first_name = member["first_name"]
        if (not first_name):
            first_name = "NULL"

        if (not user):
            Member.create(
                user_id=member["id"],
                first_name=first_name,
                username=member["username"],
            )
        else:
            user.first_name = first_name
            user.username = member["username"]
            user.save()

    group = await bot.get_chat(config.group_id)
    group_permissions = group.permissions.__dict__

    for permission in group_permissions.keys():
        config.group_permissions[permission] = group_permissions[permission]
