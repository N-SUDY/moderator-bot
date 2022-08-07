import json

from aiogram import Dispatcher,Bot
from environs import Env

env = Env()
env.read_env()

use_webhook = True

# bot token
token = env.str("bot_token")

group_id = env.str("group_id")
telegram_log_chat_id = env.str("log_group_id")

# Telegram Application
api_id = env.str("api_id")
api_hash = env.str("api_hash")

# Virus Total API
vt_api = env.str("vt_api")

with open("config/roles.json","r") as jsonfile:
    roles = json.load(jsonfile)

db_url = env.str("db_url")

# telegram-bot-api-service
telegram_api_server = env.str("telegram_api_server").split(":")
telegram_api_server = {
    "ip":telegram_api_server[0],
    "port":telegram_api_server[1]
}

telegram_api_server = f"http://{telegram_api_server['ip']}:{telegram_api_server['port']}"
