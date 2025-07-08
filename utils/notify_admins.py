import logging
from aiogram import Dispatcher
from data.config import ADMINS

async def on_startup_notify(dp: Dispatcher, message: str = None):
    """Bot ishga tushganda yoki yangi foydalanuvchi qo'shilganda adminlarga xabar yuborish."""
    if message is None:
        message = "Bot ishga tushdi!"
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, message)
        except Exception as err:
            logging.exception(f"Admin {admin} ga xabar yuborishda xatolik: {err}")