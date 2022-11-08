from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from os.path import join, dirname
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

dotenv_path = join(dirname(__file__), './.env')
load_dotenv(dotenv_path)
bot = Bot(os.environ['TOKEN_BOT'])
dp = Dispatcher(bot, storage=storage)
