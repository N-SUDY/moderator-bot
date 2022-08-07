import asyncio

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import utils
import filters

from database.database import Database


database = Database()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

storage = MemoryStorage()

tgc = utils.TelegramClientScrapper(config.api_id, config.api_hash, token=config.token, loop = loop)

bot = Bot(
    token=config.token,
    server=TelegramAPIServer.from_base(config.telegram_api_server)
)

dp = Dispatcher(bot, storage = storage)

dp.filters_factory.bind(filters.IsAdminFilter)
dp.filters_factory.bind(filters.ReplayMessageFilter)
dp.filters_factory.bind(filters.UserHasRights)
