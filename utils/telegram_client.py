from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import PeerChannel


class TelegramClientScrapper:
    def __init__(self, api_id, api_hash, phone=None, token=None, loop=None):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.loop = loop
        self.token = token
        
    async def _connect(self):
        self.client = TelegramClient("session", self.api_id, self.api_hash, loop=self.loop)
        await self.client.start(bot_token=self.token)
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input("Enter you just recieved:"))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input("Enter password:"))   

    async def get_group_users(self, group_id):
        
        chat_entity = PeerChannel(int(group_id))

        offset = 0
        limit = 100
        list_participants = []


        while True:
            participants = await self.client(GetParticipantsRequest(
                chat_entity, ChannelParticipantsSearch(''), offset, limit,
                hash=0
            ))
            
            if (not participants.users):
                break
            
            list_participants.extend(participants.users)
            offset += len(participants.users)
            
        participants_details = []
        for participant in list_participants:
            is_bot = participant.bot
            user_name = participant.username
            if (user_name):
                user_name = f"@{user_name}"
            
            if (not is_bot):
                participants_details.append({
                    "id": participant.id, 
                    "first_name": participant.first_name,
                    "user_name":user_name
                })
        
        return participants_details
