from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import utils

storage = MemoryStorage()

# Create client connection
tgc = utils.TelegramClient(config.api_id, config.api_hash, config.token)

bot = Bot(
    token=config.token,
    server=TelegramAPIServer.from_base(config.telegram_api_server),
)

dp = Dispatcher(bot, storage=storage)
