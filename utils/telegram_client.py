from pyrogram.client import Client

class TelegramClient:
    def __init__(self,api_id,api_hash,token):
        self.api_id = api_id
        self.api_hash = api_hash
        self.token = token
            
        self.client = Client("session",
            api_id=self.api_id,api_hash=self.api_hash,
            bot_token=self.token
        )


    async def members_list(self,chat_id:int):
        members = []

        async for member in self.client.get_chat_members(chat_id):
            
            try:
                username = member.user.username
            except AttributeError:
                username = None
            
            if not (username is None):
                username = f"@{username}"
            
            if (not member.user.is_bot):

                members.append({
                    "id":member.user.id,
                    "status":str(member.status),
                    "first_name":member.user.first_name,
                    "username":username,
                })  

        return members
