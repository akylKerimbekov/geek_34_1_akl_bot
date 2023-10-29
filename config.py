from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config
from aiogram import Bot, Dispatcher

TOKEN = config("TOKEN")
ROOT_PATH = config("DESTINATION")
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
