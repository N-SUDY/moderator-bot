from aiogram import Dispatcher,Bot
from environs import Env

env = Env()
env.read_env()

use_webhook = True

# bot token
token = env.str("bot_token")

group_id = env.str("group_id")
second_group_id = env.str("second_group_id")

# Telegram Application
api_id = env.int("api_id")
api_hash = env.str("api_hash")

# Virus Total API
vt_api = env.str("vt_api")

group_permissions = {
    "can_send_messages":True,
    "can_send_media_messages":False,
    "can_send_other_messages":True,
    "can_send_polls":False,
    "can_invite_users":False,
    "can_change_info":False,
    "can_add_web_page_previews":False,
    "can_pin_messages":False
}

db_url = env.str("db_url")

# telegram-bot-api-service
telegram_api_server = env.str("telegram_api_server").split(":")
telegram_api_server = {
    "ip":telegram_api_server[0],
    "port":telegram_api_server[1]
}

telegram_api_server = f"http://{telegram_api_server['ip']}:{telegram_api_server['port']}"
