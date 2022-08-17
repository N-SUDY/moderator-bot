from database.models import Member
from config import group_id

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
