from .database import Database
import logging
from typing import Optional

class LanguageDatabase(Database):
    def __init__(self, path_to_db: str):
        super().__init__(path_to_db)
        logging.info(f"LanguageDatabase initialized with path: {path_to_db}")

    def add_language_column(self) -> None:
        """Users jadvaliga language ustunini qo'shadi."""
        sql = """
            ALTER TABLE Users 
            ADD COLUMN language VARCHAR(10) DEFAULT 'uz'
        """
        try:
            self.execute(sql, commit=True)
            logging.info("Language column added to Users table")
        except Exception as e:
            if "duplicate column name" not in str(e).lower():
                logging.error(f"Error adding language column: {e}")
                raise

    def update_user_language(self, telegram_id: int, language: str) -> None:
        """Foydalanuvchi tilini yangilaydi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        sql = """
            UPDATE Users 
            SET language = ? 
            WHERE telegram_id = ?
        """
        self.execute(sql, parameters=(language, telegram_id), commit=True)
        logging.info(f"User language updated: telegram_id={telegram_id}, language={language}")

    def get_user_language(self, telegram_id: int) -> str:
        """Foydalanuvchi tilini qaytaradi."""
        sql = """
            SELECT language 
            FROM Users 
            WHERE telegram_id = ?
        """
        result = self.execute(sql, parameters=(telegram_id,), fetchone=True)
        language = result[0] if result else 'uz'
        logging.info(f"User language retrieved: telegram_id={telegram_id}, language={language}")
        return language