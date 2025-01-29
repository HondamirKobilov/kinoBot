from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

bot = Bot(token=config.BOT_TOKEN1, parse_mode=types.ParseMode.HTML)
bot2 = Bot(token=config.BOT_TOKEN2, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp2 = Dispatcher(bot2, storage=storage)
