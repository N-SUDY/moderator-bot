from database.models import Member
from config import group_id

# async def __is_group_owner(user_id):
#     from load import bot
#     member = await bot.get_chat_member(group_id,user_id)
#     return member.is_chat_owner()

async def check_user_data():
    """Check user data in database and update it"""
    from load import tgc,database
    
    members = await tgc.members_list(group_id)

    for member in members:
        exists = database.check_data_exists(Member.user_id,member["id"])
        
        role = "member"
        if (member["status"] == "ChatMemberStatus.OWNER"):
            role = "owner"

        if (not exists):
            database.register_user(
                member["id"],member["first_name"],
                member["username"],role
            )
        else:
            database.update_member_data(
                member["id"],
                [Member.first_name,Member.user_name],
                [member["first_name"],member["username"]]
            )
# async def check_user_data():
#     """Check user data in database and update it"""
#     from load import tgc,database
#     users = await tgc.get_group_users(group_id)
#
#     for user in users:
#         user_exists = database.check_data_exists(Member.user_id,user["id"])
#         
#         role = "member"
#         if (await __is_group_owner(user["id"])):role = "owner"
#
#         if (not user_exists):
#             user_name = user["user_name"]
#             
#             if (user_name):
#                 user_name = f"@{user_name}"
#             
#             database.register_user(
#                 user["id"],
#                 user["first_name"],
#                 user["user_name"],
#                 role,
#             )
#         
#         else:
#             database.update_member_data(user["id"],
#                 [Member.first_name,Member.user_name],
#                 [user["first_name",user["user_name"]]]
#             )
