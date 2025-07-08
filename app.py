
import logging
from aiogram import executor
from loader import dp, user_db, sections_db, payment_db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.config import ADMINS

# Logger sozlash
logging.basicConfig(level=logging.INFO)

async def on_startup(dispatcher):
    """Botni ishga tushirishda bajariladigan funksiya"""
    await set_default_commands(dispatcher)

    try:
        # Barcha jadvallarni yaratish
        await user_db.create_table_users()
        await payment_db.create_table_payments()
        await sections_db.create_table_questions()
        await sections_db.create_table_road_signs()
        await sections_db.create_table_truck_parts()
        logging.info("Barcha jadvallar muvaffaqiyatli yaratildi yoki allaqachon mavjud.")

        # Adminlarni o'rnatish
        for admin_id in ADMINS:
            admin_id = int(admin_id)  # ID ni int ga aylantirish
            user = await user_db.select_user(telegram_id=admin_id)
            if user:
                await user_db.set_admin(telegram_id=admin_id)
                logging.info(f"Admin o'rnatildi: telegram_id={admin_id}")
            else:
                logging.warning(f"Admin topilmadi va qo'shildi: telegram_id={admin_id}")
                await user_db.add_user(telegram_id=admin_id, username="Admin", dispatcher=dispatcher)
                await user_db.set_admin(telegram_id=admin_id)
    except Exception as e:
        logging.error(f"Jadval yaratish yoki admin o'rnatishda xatolik: {e}")
        raise

    await on_startup_notify(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
