
import sqlite3
from datetime import datetime, timedelta
import pytz
from typing import Optional, List, Dict, Any
from aiogram import Dispatcher
import logging

from data.config import ADMINS


class UserDatabase:
    def __init__(self, path_to_db: str):
        self.path_to_db = path_to_db
        self.uzbekistan_tz = pytz.timezone("Asia/Tashkent")
        logging.info(f"UserDatabase initialized with path: {path_to_db}")

    def execute(self, sql: str, parameters: tuple = (), fetchone: bool = False, fetchall: bool = False, commit: bool = False) -> Optional[List[Dict[str, Any]]]:
        """Execute a SQL query with the given parameters."""
        try:
            with sqlite3.connect(self.path_to_db) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(sql, parameters)
                if commit:
                    conn.commit()
                if fetchone:
                    result = cursor.fetchone()
                    return dict(result) if result else None
                if fetchall:
                    result = cursor.fetchall()
                    return [dict(row) for row in result] if result else []
                return None
        except Exception as e:
            logging.error(f"SQL error: {e}, query: {sql}")
            raise

    async def create_table_users(self) -> None:
        """Foydalanuvchilar jadvalini yaratadi."""
        sql = """
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id BIGINT NOT NULL UNIQUE,
                username VARCHAR(255),
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME,
                is_admin BOOLEAN NOT NULL DEFAULT 0,
                is_allowed BOOLEAN NOT NULL DEFAULT 0,
                language VARCHAR(10) NOT NULL DEFAULT 'uz'
            );
        """
        self.execute(sql, commit=True)
        logging.info("Users table created or already exists.")

    async def add_user(self, telegram_id: int, username: Optional[str] = None, dispatcher: Optional[Dispatcher] = None) -> None:
        """Foydalanuvchi qo‘shadi va adminlarga xabar yuboradi."""
        try:
            created_at = self._get_current_time().isoformat()
            username = username or "Unknown"
            is_admin = 1 if str(telegram_id) in ADMINS else 0
            sql = """
                INSERT OR IGNORE INTO Users (telegram_id, username, created_at, is_allowed, is_admin, language)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            self.execute(sql, parameters=(telegram_id, username, created_at, 0, is_admin, 'uz'), commit=True)
            logging.info(f"User added: telegram_id={telegram_id}, username={username}, is_admin={is_admin}")

            total_users = await self.count_users()
            if dispatcher:
                from utils.notify_admins import on_startup_notify  # Import here to avoid circular import
                message = (
                    f"Yangi foydalanuvchi qo'shildi!\n"
                    f"ID: {telegram_id}\n"
                    f"Username: {username}\n"
                    f"Jami foydalanuvchilar: {total_users}\n"
                    f"Ruxsat: {'Berilmagan' if not await self.check_if_allowed(telegram_id) else 'Berilgan'}\n"
                    f"Admin: {'Ha' if is_admin else 'Yo‘q'}"
                )
                await on_startup_notify(dispatcher, message=message)
                logging.info(f"Notification sent to admins: {message}")
        except Exception as e:
            logging.error(f"Error adding user: telegram_id={telegram_id}, error={e}")
            raise

    async def select_all_users(self) -> List[Dict[str, Any]]:
        """Barcha foydalanuvchilarni qaytaradi."""
        sql = "SELECT * FROM Users"
        result = self.execute(sql, fetchall=True)
        return result

    async def count_users(self) -> int:
        """Foydalanuvchilar sonini qaytaradi."""
        sql = "SELECT COUNT(*) FROM Users"
        result = self.execute(sql, fetchone=True)
        return result['COUNT(*)'] if result else 0

    async def select_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Telegram ID bo‘yicha foydalanuvchini qaytaradi."""
        try:
            sql = "SELECT * FROM Users WHERE telegram_id = ?"
            result = self.execute(sql, parameters=(telegram_id,), fetchone=True)
            return result
        except Exception as e:
            logging.error(f"Error selecting user: telegram_id={telegram_id}, error={e}")
            return None

    async def count_daily_users(self) -> int:
        """Kunlik yangi foydalanuvchilar sonini qaytaradi."""
        now = self._get_current_time()
        today_start = self._get_start_of_day(now)
        tomorrow_start = today_start + timedelta(days=1)
        sql = "SELECT COUNT(*) FROM Users WHERE created_at >= ? AND created_at < ?"
        result = self.execute(sql, parameters=(today_start.isoformat(), tomorrow_start.isoformat()), fetchone=True)
        return result['COUNT(*)'] if result else 0

    async def count_weekly_users(self) -> int:
        """Haftalik yangi foydalanuvchilar sonini qaytaradi."""
        now = self._get_current_time()
        one_week_ago = now - timedelta(days=7)
        sql = "SELECT COUNT(*) FROM Users WHERE created_at >= ?"
        result = self.execute(sql, parameters=(one_week_ago.isoformat()), fetchone=True)
        return result['COUNT(*)'] if result else 0

    async def count_monthly_users(self) -> int:
        """Oylik yangi foydalanuvchilar sonini qaytaradi."""
        now = self._get_current_time()
        one_month_ago = now - timedelta(days=30)
        sql = "SELECT COUNT(*) FROM Users WHERE created_at >= ?"
        result = self.execute(sql, parameters=(one_month_ago.isoformat()), fetchone=True)
        return result['COUNT(*)'] if result else 0

    async def update_last_active(self, telegram_id: int) -> None:
        """Foydalanuvchining so‘nggi faollik vaqtini yangilaydi."""
        try:
            last_active = self._get_current_time().isoformat()
            sql = "UPDATE Users SET last_active = ? WHERE telegram_id = ?"
            self.execute(sql, parameters=(last_active, telegram_id), commit=True)
            logging.info(f"Last active updated: telegram_id={telegram_id}, last_active={last_active}")
        except Exception as e:
            logging.error(f"Error updating last active: telegram_id={telegram_id}, error={e}")
            raise

    async def count_active_daily_users(self) -> int:
        """Kunlik faol foydalanuvchilar sonini qaytaradi."""
        now = self._get_current_time()
        today_start = self._get_start_of_day(now)
        tomorrow_start = today_start + timedelta(days=1)
        sql = "SELECT COUNT(*) FROM Users WHERE last_active >= ? AND last_active < ?"
        result = self.execute(sql, parameters=(today_start.isoformat(), tomorrow_start.isoformat()), fetchone=True)
        return result['COUNT(*)'] if result else 0

    async def count_active_weekly_users(self) -> int:
        """Haftalik faol foydalanuvchilar sonini qaytaradi."""
        now = self._get_current_time()
        one_week_ago = now - timedelta(days=7)
        sql = "SELECT COUNT(*) FROM Users WHERE last_active >= ?"
        result = self.execute(sql, parameters=(one_week_ago.isoformat()), fetchone=True)
        return result['COUNT(*)'] if result else 0

    async def count_monthly_users(self) -> int:
        """Oylik faol foydalanuvchilar sonini qaytaradi."""
        now = self._get_current_time()
        one_month_ago = now - timedelta(days=30)
        sql = "SELECT COUNT(*) FROM Users WHERE last_active >= ?"
        result = self.execute(sql, parameters=(one_month_ago.isoformat()), fetchone=True)
        return result['COUNT(*)'] if result else 0

    async def check_if_admin(self, telegram_id: int) -> bool:
        """Foydalanuvchi admin ekanligini tekshiradi."""
        try:
            sql = "SELECT is_admin FROM Users WHERE telegram_id = ?"
            result = self.execute(sql, parameters=(telegram_id,), fetchone=True)
            return bool(result and result['is_admin'])
        except Exception as e:
            logging.error(f"Error checking admin status: telegram_id={telegram_id}, error={e}")
            return False

    async def check_if_allowed(self, telegram_id: int) -> bool:
        """Foydalanuvchi ruxsatga ega ekanligini tekshiradi."""
        try:
            sql = "SELECT is_allowed FROM Users WHERE telegram_id = ?"
            result = self.execute(sql, parameters=(telegram_id,), fetchone=True)
            return bool(result and result['is_allowed'])
        except Exception as e:
            logging.error(f"Error checking permission: telegram_id={telegram_id}, error={e}")
            return False

    async def update_user_permission(self, telegram_id: int, is_allowed: bool) -> None:
        """Foydalanuvchi ruxsatini yangilaydi."""
        try:
            sql = "UPDATE Users SET is_allowed = ? WHERE telegram_id = ?"
            self.execute(sql, parameters=(int(is_allowed), telegram_id), commit=True)
            logging.info(f"Permission updated: telegram_id={telegram_id}, is_allowed={is_allowed}")
        except Exception as e:
            logging.error(f"Error updating permission: telegram_id={telegram_id}, error={e}")
            raise

    async def set_admin(self, telegram_id: int) -> None:
        """Foydalanuvchini admin qiladi."""
        try:
            sql = "UPDATE Users SET is_admin = 1 WHERE telegram_id = ?"
            self.execute(sql, parameters=(telegram_id,), commit=True)
            logging.info(f"User set as admin: telegram_id={telegram_id}")
        except Exception as e:
            logging.error(f"Error setting admin: telegram_id={telegram_id}, error={e}")
            raise

    async def update_user_language(self, telegram_id: int, language: str) -> None:
        """Foydalanuvchi tilini yangilaydi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        try:
            sql = "UPDATE Users SET language = ? WHERE telegram_id = ?"
            self.execute(sql, parameters=(language, telegram_id), commit=True)
            logging.info(f"Language updated: telegram_id={telegram_id}, language={language}")
        except Exception as e:
            logging.error(f"Error updating language: telegram_id={telegram_id}, error={e}")
            raise

    async def get_user_language(self, telegram_id: int) -> str:
        """Foydalanuvchi tilini qaytaradi."""
        try:
            sql = "SELECT language FROM Users WHERE telegram_id = ?"
            result = self.execute(sql, parameters=(telegram_id,), fetchone=True)
            return result['language'] if result else 'uz'
        except Exception as e:
            logging.error(f"Error getting language: telegram_id={telegram_id}, error={e}")
            return 'uz'

    def _get_current_time(self) -> datetime:
        """Joriy vaqtni O‘zbekiston vaqt mintaqasida oladi."""
        return datetime.now(self.uzbekistan_tz)

    def _get_start_of_day(self, date: datetime) -> datetime:
        """Kun boshlanish vaqtini oladi."""
        return date.replace(hour=0, minute=0, second=0, microsecond=0)
