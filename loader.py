
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.users import UserDatabase
from utils.db_api.sections import SectionsDatabase
from utils.db_api.payment import PaymentDatabase
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
user_db = UserDatabase(path_to_db="data/user.db")
payment_db = PaymentDatabase(path_to_db="data/payment.db")
sections_db = SectionsDatabase(path_to_db="data/sections.db")
