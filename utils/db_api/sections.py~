import sqlite3
import logging
from typing import List, Dict, Any, Optional


class SectionsDatabase:
    def __init__(self, path_to_db: str):
        self.path_to_db = path_to_db
        logging.info(f"SectionsDatabase initialized with path: {path_to_db}")

    def execute(self, sql: str, parameters: tuple = (), fetchone: bool = False, fetchall: bool = False,
                commit: bool = False) -> Any:
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
        except sqlite3.Error as e:
            logging.error(f"SQL error in execute: {e}, query: {sql}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in execute: {e}, query: {sql}")
            raise

    async def create_table_questions(self) -> None:
        """Savol-javoblar jadvalini yaratadi."""
        sql_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='Questions'"
        result = self.execute(sql_check, fetchone=True)
        if not result:
            sql_create = """
                CREATE TABLE IF NOT EXISTS Questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    display_id INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    audio_file_id VARCHAR(255) NULL,
                    language VARCHAR(10) NOT NULL CHECK(language IN ('uz', 'ru', 'es'))
                );
            """
            self.execute(sql_create, commit=True)
            logging.info("Questions table created.")
        else:
            sql_check_column = "PRAGMA table_info(Questions)"
            columns = self.execute(sql_check_column, fetchall=True)
            has_display_id = any(col['name'] == 'display_id' for col in columns)
            if not has_display_id:
                self.execute("ALTER TABLE Questions RENAME TO Questions_old", commit=True)
                sql_create = """
                    CREATE TABLE IF NOT EXISTS Questions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        display_id INTEGER NOT NULL,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        audio_file_id VARCHAR(255) NULL,
                        language VARCHAR(10) NOT NULL CHECK(language IN ('uz', 'ru', 'es'))
                    );
                """
                self.execute(sql_create, commit=True)
                self.execute("""
                    INSERT INTO Questions (id, display_id, question, answer, audio_file_id, language)
                    SELECT id, ROW_NUMBER() OVER (PARTITION BY language ORDER BY id) AS display_id, 
                           question, answer, audio_file_id, language 
                    FROM Questions_old
                """, commit=True)
                self.execute("DROP TABLE Questions_old", commit=True)
                logging.info("Questions table migrated with display_id column.")

            # Tillarda alohida ketma-ketlik yaratish
            languages = ['uz', 'ru', 'es']
            for lang in languages:
                await self._reindex_display_ids("Questions", lang)
            logging.info("Questions table display_ids reindexed for all languages.")

    async def create_table_road_signs(self) -> None:
        """Yo'l belgilari jadvalini yaratadi."""
        sql_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='RoadSigns'"
        result = self.execute(sql_check, fetchone=True)
        if not result:
            sql_create = """
                CREATE TABLE IF NOT EXISTS RoadSigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    display_id INTEGER NOT NULL,
                    image_file_id VARCHAR(255) NOT NULL,
                    description TEXT NULL,
                    language VARCHAR(10) NOT NULL CHECK(language IN ('uz', 'ru', 'es'))
                );
            """
            self.execute(sql_create, commit=True)
            logging.info("RoadSigns table created.")
        else:
            sql_check_column = "PRAGMA table_info(RoadSigns)"
            columns = self.execute(sql_check_column, fetchall=True)
            has_display_id = any(col['name'] == 'display_id' for col in columns)
            if not has_display_id:
                self.execute("ALTER TABLE RoadSigns RENAME TO RoadSigns_old", commit=True)
                sql_create = """
                    CREATE TABLE IF NOT EXISTS RoadSigns (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        display_id INTEGER NOT NULL,
                        image_file_id VARCHAR(255) NOT NULL,
                        description TEXT NULL,
                        language VARCHAR(10) NOT NULL CHECK(language IN ('uz', 'ru', 'es'))
                    );
                """
                self.execute(sql_create, commit=True)
                self.execute("""
                    INSERT INTO RoadSigns (id, display_id, image_file_id, description, language)
                    SELECT id, ROW_NUMBER() OVER (PARTITION BY language ORDER BY id) AS display_id, 
                           image_file_id, description, language 
                    FROM RoadSigns_old
                """, commit=True)
                self.execute("DROP TABLE RoadSigns_old", commit=True)
                logging.info("RoadSigns table migrated with display_id column.")

            # Tillarda alohida ketma-ketlik yaratish
            languages = ['uz', 'ru', 'es']
            for lang in languages:
                await self._reindex_display_ids("RoadSigns", lang)
            logging.info("RoadSigns table display_ids reindexed for all languages.")

    async def create_table_truck_parts(self) -> None:
        """Yuk mashinasi qismlari jadvalini yaratadi."""
        sql_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='TruckParts'"
        result = self.execute(sql_check, fetchone=True)
        if not result:
            sql_create = """
                CREATE TABLE IF NOT EXISTS TruckParts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    display_id INTEGER NOT NULL,
                    image_file_id VARCHAR(255) NOT NULL,
                    description TEXT NULL,
                    language VARCHAR(10) NOT NULL CHECK(language IN ('uz', 'ru', 'es'))
                );
            """
            self.execute(sql_create, commit=True)
            logging.info("TruckParts table created.")
        else:
            sql_check_column = "PRAGMA table_info(TruckParts)"
            columns = self.execute(sql_check_column, fetchall=True)
            has_display_id = any(col['name'] == 'display_id' for col in columns)
            if not has_display_id:
                self.execute("ALTER TABLE TruckParts RENAME TO TruckParts_old", commit=True)
                sql_create = """
                    CREATE TABLE IF NOT EXISTS TruckParts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        display_id INTEGER NOT NULL,
                        image_file_id VARCHAR(255) NOT NULL,
                        description TEXT NULL,
                        language VARCHAR(10) NOT NULL CHECK(language IN ('uz', 'ru', 'es'))
                    );
                """
                self.execute(sql_create, commit=True)
                self.execute("""
                    INSERT INTO TruckParts (id, display_id, image_file_id, description, language)
                    SELECT id, ROW_NUMBER() OVER (PARTITION BY language ORDER BY id) AS display_id, 
                           image_file_id, description, language 
                    FROM TruckParts_old
                """, commit=True)
                self.execute("DROP TABLE TruckParts_old", commit=True)
                logging.info("TruckParts table migrated with display_id column.")

            # Tillarda alohida ketma-ketlik yaratish
            languages = ['uz', 'ru', 'es']
            for lang in languages:
                await self._reindex_display_ids("TruckParts", lang)
            logging.info("TruckParts table display_ids reindexed for all languages.")

    async def _get_next_display_id(self, table: str, language: str) -> int:
        """Muayyan jadval va til uchun keyingi display_id ni qaytaradi."""
        sql = f"SELECT MAX(display_id) AS max_id FROM {table} WHERE language = ?"
        result = self.execute(sql, parameters=(language,), fetchone=True)
        max_id = result['max_id'] if result and result['max_id'] is not None else 0
        return max_id + 1

    async def _reindex_display_ids(self, table: str, language: str) -> None:
        """Muayyan jadval va til uchun display_id larni qayta indekslaydi."""
        sql = f"SELECT id FROM {table} WHERE language = ? ORDER BY id"
        items = self.execute(sql, parameters=(language,), fetchall=True)
        for new_display_id, item in enumerate(items, 1):
            update_sql = f"UPDATE {table} SET display_id = ? WHERE id = ?"
            self.execute(update_sql, parameters=(new_display_id, item['id']), commit=True)
        logging.info(f"Display IDs reindexed for table={table}, language={language}, count={len(items)}")

    async def add_question(self, question: str, answer: str, audio_file_id: str = None, language: str = 'uz') -> int:
        """Savol-javob qo'shadi va shu tildagi ketma-ketlikni saqlaydi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")

        display_id = await self._get_next_display_id("Questions", language)
        sql = """
            INSERT INTO Questions (display_id, question, answer, audio_file_id, language)
            VALUES (?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(display_id, question, answer, audio_file_id, language), commit=True)
        result = self.execute("SELECT last_insert_rowid()", fetchone=True)
        question_id = result['last_insert_rowid()'] if result else None
        logging.info(
            f"Savol qo'shildi: question={question[:50]}, language={language}, question_id={question_id}, display_id={display_id}")
        return question_id

    async def add_road_sign(self, image_file_id: str, description: str = None, language: str = 'uz') -> int:
        """Yo'l belgisi qo'shadi va shu tildagi ketma-ketlikni saqlaydi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        if not image_file_id:
            raise ValueError("Image file ID cannot be empty")

        display_id = await self._get_next_display_id("RoadSigns", language)
        sql = """
            INSERT INTO RoadSigns (display_id, image_file_id, description, language)
            VALUES (?, ?, ?, ?)
        """
        self.execute(sql, parameters=(display_id, image_file_id, description, language), commit=True)
        result = self.execute("SELECT last_insert_rowid()", fetchone=True)
        sign_id = result['last_insert_rowid()'] if result else None
        logging.info(
            f"Yo'l belgisi qo'shildi: image_file_id={image_file_id}, language={language}, sign_id={sign_id}, display_id={display_id}")
        return sign_id

    async def add_truck_part(self, image_file_id: str, description: str = None, language: str = 'uz') -> int:
        """Yuk mashinasi qismini qo'shadi va shu tildagi ketma-ketlikni saqlaydi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        if not image_file_id:
            raise ValueError("Image file ID cannot be empty")

        display_id = await self._get_next_display_id("TruckParts", language)
        sql = """
            INSERT INTO TruckParts (display_id, image_file_id, description, language)
            VALUES (?, ?, ?, ?)
        """
        self.execute(sql, parameters=(display_id, image_file_id, description, language), commit=True)
        result = self.execute("SELECT last_insert_rowid()", fetchone=True)
        part_id = result['last_insert_rowid()'] if result else None
        logging.info(
            f"Truck zapchasti qo'shildi: image_file_id={image_file_id}, language={language}, part_id={part_id}, display_id={display_id}")
        return part_id

    async def update_question(self, question_id: int, question: str = None, answer: str = None,
                              audio_file_id: str = None, language: str = None) -> None:
        """Savol-javobni yangilaydi."""
        if language and language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")

        # Eski tilni olish
        old_question = await self.get_question_by_id(question_id)
        if not old_question:
            raise ValueError(f"Question with ID {question_id} not found")

        old_language = old_question['language']

        updates = []
        params = []
        if question:
            updates.append("question = ?")
            params.append(question)
        if answer:
            updates.append("answer = ?")
            params.append(answer)
        if audio_file_id:
            updates.append("audio_file_id = ?")
            params.append(audio_file_id)
        if language:
            updates.append("language = ?")
            params.append(language)
        if not updates:
            raise ValueError("No fields to update")

        params.append(question_id)
        sql = f"UPDATE Questions SET {', '.join(updates)} WHERE id = ?"
        self.execute(sql, parameters=tuple(params), commit=True)

        # Agar til o'zgartirilgan bo'lsa, ikkala tilda ham qayta indekslash
        if language and language != old_language:
            await self._reindex_display_ids("Questions", old_language)
            await self._reindex_display_ids("Questions", language)
        elif language:
            await self._reindex_display_ids("Questions", language)

        logging.info(f"Savol yangilandi: question_id={question_id}")

    async def update_road_sign(self, sign_id: int, image_file_id: str = None, description: str = None,
                               language: str = None) -> None:
        """Yo'l belgisini yangilaydi."""
        if language and language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")

        # Eski tilni olish
        old_sign = await self.get_road_sign_by_id(sign_id)
        if not old_sign:
            raise ValueError(f"Road sign with ID {sign_id} not found")

        old_language = old_sign['language']

        updates = []
        params = []
        if image_file_id:
            updates.append("image_file_id = ?")
            params.append(image_file_id)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if language:
            updates.append("language = ?")
            params.append(language)
        if not updates:
            raise ValueError("No fields to update")

        params.append(sign_id)
        sql = f"UPDATE RoadSigns SET {', '.join(updates)} WHERE id = ?"
        self.execute(sql, parameters=tuple(params), commit=True)

        # Agar til o'zgartirilgan bo'lsa, ikkala tilda ham qayta indekslash
        if language and language != old_language:
            await self._reindex_display_ids("RoadSigns", old_language)
            await self._reindex_display_ids("RoadSigns", language)
        elif language:
            await self._reindex_display_ids("RoadSigns", language)

        logging.info(f"Yo'l belgisi yangilandi: sign_id={sign_id}")

    async def update_truck_part(self, part_id: int, image_file_id: str = None, description: str = None,
                                language: str = None) -> None:
        """Yuk mashinasi qismini yangilaydi."""
        if language and language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")

        # Eski tilni olish
        old_part = await self.get_truck_part_by_id(part_id)
        if not old_part:
            raise ValueError(f"Truck part with ID {part_id} not found")

        old_language = old_part['language']

        updates = []
        params = []
        if image_file_id:
            updates.append("image_file_id = ?")
            params.append(image_file_id)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if language:
            updates.append("language = ?")
            params.append(language)
        if not updates:
            raise ValueError("No fields to update")

        params.append(part_id)
        sql = f"UPDATE TruckParts SET {', '.join(updates)} WHERE id = ?"
        self.execute(sql, parameters=tuple(params), commit=True)

        # Agar til o'zgartirilgan bo'lsa, ikkala tilda ham qayta indekslash
        if language and language != old_language:
            await self._reindex_display_ids("TruckParts", old_language)
            await self._reindex_display_ids("TruckParts", language)
        elif language:
            await self._reindex_display_ids("TruckParts", language)

        logging.info(f"Truck zapchasti yangilandi: part_id={part_id}")

    async def get_questions(self, language: str) -> List[Dict[str, Any]]:
        """Til bo'yicha savol-javoblarni qaytaradi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        sql = "SELECT id, display_id, question, answer, audio_file_id, language FROM Questions WHERE language = ? ORDER BY display_id"
        result = self.execute(sql, parameters=(language,), fetchall=True)
        return result or []

    async def get_road_signs(self, language: str) -> List[Dict[str, Any]]:
        """Til bo'yicha yo'l belgilarini qaytaradi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        sql = "SELECT id, display_id, image_file_id, description, language FROM RoadSigns WHERE language = ? ORDER BY display_id"
        result = self.execute(sql, parameters=(language,), fetchall=True)
        return result or []

    async def get_truck_parts(self, language: str) -> List[Dict[str, Any]]:
        """Til bo'yicha yuk mashinasi qismlarini qaytaradi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        sql = "SELECT id, display_id, image_file_id, description, language FROM TruckParts WHERE language = ? ORDER BY display_id"
        result = self.execute(sql, parameters=(language,), fetchall=True)
        return result or []

    async def get_question_by_id(self, question_id: int, language: str = 'uz') -> Optional[Dict[str, Any]]:
        """Savolni ID va til bo'yicha qaytaradi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        sql = "SELECT id, display_id, question, answer, audio_file_id, language FROM Questions WHERE id = ? AND language = ?"
        result = self.execute(sql, parameters=(question_id, language), fetchone=True)
        return result

    async def get_road_sign_by_id(self, sign_id: int, language: str = 'uz') -> Optional[Dict[str, Any]]:
        """Yo'l belgisini ID va til bo'yicha qaytaradi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        sql = "SELECT id, display_id, image_file_id, description, language FROM RoadSigns WHERE id = ? AND language = ?"
        result = self.execute(sql, parameters=(sign_id, language), fetchone=True)
        return result

    async def get_truck_part_by_id(self, part_id: int, language: str = 'uz') -> Optional[Dict[str, Any]]:
        """Yuk mashinasi qismini ID va til bo'yicha qaytaradi."""
        if language not in ['uz', 'ru', 'es']:
            raise ValueError(f"Invalid language code: {language}")
        sql = "SELECT id, display_id, image_file_id, description, language FROM TruckParts WHERE id = ? AND language = ?"
        result = self.execute(sql, parameters=(part_id, language), fetchone=True)
        return result

    async def delete_question(self, question_id: int) -> None:
        """Savolni o'chiradi va shu tildagi display_id larni qayta indekslaydi."""
        question = await self.get_question_by_id(question_id)
        if question:
            language = question['language']
            sql = "DELETE FROM Questions WHERE id = ?"
            self.execute(sql, parameters=(question_id,), commit=True)
            await self._reindex_display_ids("Questions", language)
            logging.info(f"Savol o'chirildi: question_id={question_id}, language={language}")

    async def delete_road_sign(self, sign_id: int) -> None:
        """Yo'l belgisini o'chiradi va shu tildagi display_id larni qayta indekslaydi."""
        road_sign = await self.get_road_sign_by_id(sign_id)
        if road_sign:
            language = road_sign['language']
            sql = "DELETE FROM RoadSigns WHERE id = ?"
            self.execute(sql, parameters=(sign_id,), commit=True)
            await self._reindex_display_ids("RoadSigns", language)
            logging.info(f"Yo'l belgisi o'chirildi: sign_id={sign_id}, language={language}")

    async def delete_truck_part(self, part_id: int) -> None:
        """Yuk mashinasi qismini o'chiradi va shu tildagi display_id larni qayta indekslaydi."""
        truck_part = await self.get_truck_part_by_id(part_id)
        if truck_part:
            language = truck_part['language']
            sql = "DELETE FROM TruckParts WHERE id = ?"
            self.execute(sql, parameters=(part_id,), commit=True)
            await self._reindex_display_ids("TruckParts", language)
            logging.info(f"Truck zapchasti o'chirildi: part_id={part_id}, language={language}")

    # Qo'shimcha metodlar - til bo'yicha statistika
    async def get_question_count_by_language(self, language: str) -> int:
        """Til bo'yicha savollar sonini qaytaradi."""
        sql = "SELECT COUNT(*) as count FROM Questions WHERE language = ?"
        result = self.execute(sql, parameters=(language,), fetchone=True)
        return result['count'] if result else 0

    async def get_road_sign_count_by_language(self, language: str) -> int:
        """Til bo'yicha yo'l belgilari sonini qaytaradi."""
        sql = "SELECT COUNT(*) as count FROM RoadSigns WHERE language = ?"
        result = self.execute(sql, parameters=(language,), fetchone=True)
        return result['count'] if result else 0

    async def get_truck_part_count_by_language(self, language: str) -> int:
        """Til bo'yicha yuk mashinasi qismlari sonini qaytaradi."""
        sql = "SELECT COUNT(*) as count FROM TruckParts WHERE language = ?"
        result = self.execute(sql, parameters=(language,), fetchone=True)
        return result['count'] if result else 0