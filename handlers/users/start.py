
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp, bot, user_db, sections_db, payment_db
from data.config import ADMINS
import logging
import importlib
import sys
import time

logging.basicConfig(level=logging.INFO)


# States class
class UserStates(StatesGroup):
    SELECTING_LANGUAGE = State()
    WAITING_FOR_PAYMENT = State()


# To‘lov ma'lumotlari keshini boshqarish
class PaymentInfoCache:
    def __init__(self):
        self._cache = None
        self._last_updated = None
        self._cache_timeout = 60  # 1 daqiqa kesh muddati

    async def get_payment_info(self):
        """Kesh orqali to'lov ma'lumotlarini olish"""
        current_time = time.time()
        if (self._cache is None or
                self._last_updated is None or
                current_time - self._last_updated > self._cache_timeout):
            await self._refresh_cache()
        return self._cache

    async def _refresh_cache(self):
        """Keshni yangilash"""
        try:
            # data.config modulini qayta yuklash
            if 'data.config' in sys.modules:
                importlib.reload(sys.modules['data.config'])

            from data.config import PAYMENT_AMOUNT

            self._cache = {
                'amount': float(PAYMENT_AMOUNT),
                'card': "💳 *Uzcard:* *5614 6818 1201 1462*\n💳 *Visa:* *4231 2000 0805 3422*",
                'owner': "👤 Umedjon Mirbakayev"
            }
            self._last_updated = time.time()

        except Exception as e:
            logging.error(f"To'lov keshini yangilashda xatolik: {e}")
            self._cache = {
                'amount': 10.00,  # Fallback qiymat
                'card': "💳 *Uzcard:* *5614 6818 1201 1462*\n💳 *Visa:* *4231 2000 0805 3422*",
                'owner': "👤 Umedjon Mirbakayev"
            }
            self._last_updated = time.time()

    def clear_cache(self):
        """Keshni tozalash"""
        self._cache = None
        self._last_updated = None

# Global kesh obyekti
payment_cache = PaymentInfoCache()



# Enhanced localization messages
async def get_messages_async():
    """Real vaqtda xabarlarni olish"""
    payment_info = await payment_cache.get_payment_info()
    # Karta raqamlarini `\n` bilan ajratish
    card_lines = payment_info['card'].split('\n')
    uzcard_line = card_lines[0].strip() if card_lines and len(card_lines) > 0 else "Karta ma'lumoti yo'q"
    visa_line = card_lines[1].strip() if card_lines and len(card_lines) > 1 else "Karta ma'lumoti yo'q"
    return {
        "uz": {
            "welcome": "🌟 *Xush kelibsiz!* 🌟\nIltimos, o'zingiz uchun mos tilni tanlang 👇",
            "questions_answers": "📝 Savol va Javoblar",
            "road_signs": "🚦 Yo'l Belgilari",
            "truck_parts": "🚚 Truck Ehtiyot Qismlari",
            "language_settings": "⚙️ Til Sozlamalari",
            "success_message": "✅ *Tabriklaymiz!* 🎉 Botdan foydalanishingiz mumkin! 🚀",
            "payment_required": f"💰 Botdan foydalanish uchun ${payment_info['amount']} to'lov qiling va chekni yuboring 📸\n\n"
                               f"🌐 Karta ma'lumotlari:\n"
                               f"  💳 Uzcard: *{uzcard_line.split('Uzcard:')[1].strip().replace('*', '') if 'Uzcard:' in uzcard_line else uzcard_line}*\n"
                               f"  💳 Visa:   *{visa_line.split('Visa:')[1].strip().replace('*', '') if 'Visa:' in visa_line else visa_line}*\n"
                               f"👤 Karta egasi: {payment_info['owner']}",
            "select_new_language": "🌐 *Yangi tilni tanlang:* 👇",
            "language_saved": "✅ *Til saqlandi!* 🌟 Endi botni o'zingiz uchun sozlang!",
            "payment_received": "📩 *Chek qabul qilindi!* ✅ Admin tasdiqlashini kuting ⏳",
            "payment_already_pending": "⚠️ *Diqqat!* Sizning oldingi chekingiz hali ko'rib chiqilmoqda. Iltimos, kuting! ⏳",
            "no_access": "❌ *Ruxsat yo'q!* 💡 Botdan foydalanish uchun to'lov qiling.",
            "no_data": "⚠️ *Diqqat!* Bu bo'limda hozircha ma'lumot yo'q. Keling, keyinroq urinib ko'ramiz! 😊",
            "select_section": "📋 *Iltimos, menyudan bo'lim tanlang:* 👇",
            "error_occurred": "🚫 *Xatolik yuz berdi!* 😔 Iltimos, qayta urinib ko'ring.",
            "item_not_found": "🔍 *Element topilmadi!* Iltimos, boshqa elementni tanlang.",
            "forward_prohibited": "⚠️ *Forward taqiqlangan!* 🚫 Xabarni qayta yubormang.",
            "previous": "⬅️ Oldingi",
            "next": "Keyingi ➡️",
            "question": "📝 Savol",
            "road_sign": "🚦 Yo'l Belgisi",
            "truck_part": "🚚 Truck Ehtiyot Qismi",
            "questions_list": "📚 *Savol va Javoblar Ro'yxati:*",
            "road_signs_list": "🚦 *Yo'l Belgilari Ro'yxati:*",
            "truck_parts_list": "🚚 *Truck Ehtiyot Qismlari Ro'yxati:*",
            "question_label": "📌 *Savol:*",
            "answer_label": "💡 *Javob:*",
            "audio_caption": "🎵 *Savol Audiosi*",
            "back_to_menu": "🔙 Orqaga",
            "payment_rejected": "❌ *Kechirasiz, to'lovingiz rad etildi! Iltimos, qayta urinib ko'ring.*"
        },
        "ru": {
            "welcome": "🌟 *Добро пожаловать!* 🌟\nПожалуйста, выберите язык 👇",
            "questions_answers": "📝 Вопросы и ответы",
            "road_signs": "🚦 Дорожные знаки",
            "truck_parts": "🚚 Запчасти для грузовиков",
            "language_settings": "⚙️ Настройки языка",
            "success_message": "✅ *Поздравляем!* 🎉 Вы можете использовать бота! 🚀",
            "payment_required": f"💰 Оплатите ${payment_info['amount']} для использования бота и отправьте чек 📸\n\n"
                               f"🌐 Информация о карте:\n"
                               f"  💳 Uzcard: *{uzcard_line.split('Uzcard:')[1].strip().replace('*', '') if 'Uzcard:' in uzcard_line else uzcard_line}*\n"
                               f"  💳 Visa:   *{visa_line.split('Visa:')[1].strip().replace('*', '') if 'Visa:' in visa_line else visa_line}*\n"
                               f"👤 Владелец карты: {payment_info['owner']}",
            "select_new_language": "🌐 *Выберите новый язык:* 👇",
            "language_saved": "✅ *Язык сохранен!* 🌟 Настройте бота под себя!",
            "payment_received": "📩 *Чек принят!* ✅ Ожидайте подтверждения администратора ⏳",
            "payment_already_pending": "⚠️ *Внимание!* Ваш предыдущий чек еще рассматривается. Пожалуйста, подождите! ⏳",
            "no_access": "❌ *Нет доступа!* 💡 Оплатите, чтобы использовать бота.",
            "no_data": "⚠️ *Внимание!* В этом разделе пока нет данных. Попробуем позже! 😊",
            "select_section": "📋 *Выберите раздел из меню:* 👇",
            "error_occurred": "🚫 *Произошла ошибка!* 😔 Пожалуйста, попробуйте снова.",
            "item_not_found": "🔍 *Элемент не найден!* Выберите другой элемент.",
            "forward_prohibited": "⚠️ *Пересылка запрещена!* 🚫 Не отправляйте сообщения повторно.",
            "previous": "⬅️ Предыдущая",
            "next": "Следующая ➡️",
            "question": "📝 Вопрос",
            "road_sign": "🚦 Дорожный знак",
            "truck_part": "🚚 Запчасть грузовика",
            "questions_list": "📚 *Список вопросов и ответов:*",
            "road_signs_list": "🚦 *Список дорожных знаков:*",
            "truck_parts_list": "🚚 *Список запчастей для грузовиков:*",
            "question_label": "📌 *Вопрос:*",
            "answer_label": "💡 *Ответ:*",
            "audio_caption": "🎵 *Аудио вопроса*",
            "back_to_menu": "🔙 Назад",
            "payment_rejected": "❌ *К сожалению, ваш платеж отклонен! Пожалуйста, попробуйте снова.*"
        },
        "es": {
            "welcome": "🌟 *¡Bienvenido!* 🌟\nPor favor, selecciona un idioma 👇",
            "questions_answers": "📝 Preguntas y respuestas",
            "road_signs": "🚦 Señales de tráfico",
            "truck_parts": "🚚 Piezas de camiones",
            "language_settings": "⚙️ Configuración de idioma",
            "success_message": "✅ *¡Felicidades!* 🎉 ¡Puedes usar el bot! 🚀",
            "payment_required": f"💰 Paga ${payment_info['amount']} para usar el bot y envía el recibo 📸\n\n"
                               f"🌐 Información de la tarjeta:\n"
                               f"  💳 Uzcard: *{uzcard_line.split('Uzcard:')[1].strip().replace('*', '') if 'Uzcard:' in uzcard_line else uzcard_line}*\n"
                               f"  💳 Visa:   *{visa_line.split('Visa:')[1].strip().replace('*', '') if 'Visa:' in visa_line else visa_line}*\n"
                               f"👤 Titular de la tarjeta: {payment_info['owner']}",
            "select_new_language": "🌐 *Selecciona un nuevo idioma:* 👇",
            "language_saved": "✅ *¡Idioma guardado!* 🌟 ¡Personaliza el bot!",
            "payment_received": "📩 *¡Recibo recibido!* ✅ Espera la confirmación del administrador ⏳",
            "payment_already_pending": "⚠️ *¡Atención!* Tu recibo anterior aún está siendo revisado. ¡Por favor, espera! ⏳",
            "no_access": "❌ *¡Sin acceso!* 💡 Realiza el pago para usar el bot.",
            "no_data": "⚠️ *¡Atención!* No hay datos en esta sección. ¡Intentémoslo más tarde! 😊",
            "select_section": "📋 *Por favor, selecciona una sección del menú:* 👇",
            "error_occurred": "🚫 *¡Ocurrió un error!* 😔 Inténtalo de nuevo.",
            "item_not_found": "🔍 *¡Elemento no encontrado!* Selecciona otro elemento.",
            "forward_prohibited": "⚠️ *¡Reenvío prohibido!* 🚫 No reenvíes mensajes.",
            "previous": "⬅️ Anterior",
            "next": "Siguiente ➡️",
            "question": "📝 Pregunta",
            "road_sign": "🚦 Señal de tráfico",
            "truck_part": "🚚 Pieza de camión",
            "questions_list": "📚 *Lista de preguntas y respuestas:*",
            "road_signs_list": "🚦 *Lista de señales de tráfico:*",
            "truck_parts_list": "🚚 *Lista de piezas de camiones:*",
            "question_label": "📌 *Pregunta:*",
            "answer_label": "💡 *Respuesta:*",
            "audio_caption": "🎵 *Audio de la pregunta*",
            "back_to_menu": "🔙 Atrás",
            "payment_rejected": "❌ *¡Lo sentimos, tu pago ha sido rechazado! Por favor, inténtalo de nuevo.*"
        }
    }

async def get_message_async(language: str, key: str) -> str:
    """Lokalizatsiya xabarini async tarzda olish"""
    messages = await get_messages_async()
    return messages.get(language, messages["uz"]).get(key, messages["uz"].get(key, "Xabar topilmadi"))

def get_language_inline_keyboard():
    """Language selection keyboard"""
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🇺🇿 O‘zbek tili", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский язык", callback_data="lang_ru"),
        InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")
    )

async def get_main_menu(language: str):
    """Main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton(await get_message_async(language, "questions_answers")),
        KeyboardButton(await get_message_async(language, "road_signs"))
    )
    keyboard.add(
        KeyboardButton(await get_message_async(language, "truck_parts")),
        KeyboardButton(await get_message_async(language, "language_settings"))
    )
    return keyboard

async def get_pagination_buttons(section: str, page: int, total_items: int, language: str, items_per_page: int = 10):
    """Pagination buttons"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    if page > 1:
        keyboard.insert(InlineKeyboardButton(
            await get_message_async(language, "previous"),
            callback_data=f"page_{section}_{page - 1}_{language}"
        ))
    if page < total_pages:
        keyboard.insert(InlineKeyboardButton(
            await get_message_async(language, "next"),
            callback_data=f"page_{section}_{page + 1}_{language}"
        ))
    return keyboard

async def get_section_items_keyboard(items, section: str, language: str, page: int, total_items: int):
    """Section items keyboard with pagination"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in items or []:
        if item and isinstance(item, dict):
            real_id = item.get("id")
            display_id = item.get("display_id", real_id)
            content = item.get("question", item.get("description", item.get("name", "Kontent yo‘q")))
            content_preview = (content[:50] + "..." if len(str(content)) > 50 else content)
            display_text = f"#{display_id}: {content_preview}"
            keyboard.add(InlineKeyboardButton(display_text, callback_data=f"{section}_{real_id}"))
    pagination_keyboard = await get_pagination_buttons(section, page, total_items, language)
    if pagination_keyboard.inline_keyboard:
        keyboard.row(*pagination_keyboard.inline_keyboard[0])
    keyboard.add(InlineKeyboardButton(await get_message_async(language, "back_to_menu"), callback_data="back_to_menu"))
    return keyboard

async def get_section_type_from_text(text: str) -> str:
    """Determine section type from button text"""
    messages = await get_messages_async()
    section_mapping = {}
    for lang in messages:
        section_mapping[messages[lang]["questions_answers"]] = "question"
        section_mapping[messages[lang]["road_signs"]] = "road_sign"
        section_mapping[messages[lang]["truck_parts"]] = "truck_part"
    return section_mapping.get(text)

async def get_section_list_title(section: str, language: str) -> str:
    """Get section list title"""
    title_mapping = {
        "question": "questions_list",
        "road_sign": "road_signs_list",
        "truck_part": "truck_parts_list"
    }
    return await get_message_async(language, title_mapping.get(section, "select_section"))

async def is_language_settings_text(text: str) -> bool:
    """Check if text is language settings button"""
    messages = await get_messages_async()
    for lang in messages:
        if text == messages[lang]["language_settings"]:
            return True
    return False

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    """Start command handler"""
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    logging.info(f"Bot boshlandi: user_id={user_id}, username={username}")

    try:
        user = await user_db.select_user(telegram_id=user_id)
        if not user:
            await user_db.add_user(telegram_id=user_id, username=username, dispatcher=dp)
            user = await user_db.select_user(telegram_id=user_id)

        user_language = user.get("language", "uz") if user else "uz"
        is_allowed = user.get("is_allowed", False) if user else False
        is_admin = user.get("is_admin", False) if user else False

        await user_db.update_last_active(telegram_id=user_id)

        if is_admin or is_allowed:
            await message.answer(
                await get_message_async(user_language, "success_message"),
                reply_markup=await get_main_menu(user_language),
                parse_mode="Markdown",
                protect_content=True
            )
            await state.finish()
        else:
            await message.answer(
                await get_message_async(user_language, "welcome"),
                reply_markup=get_language_inline_keyboard(),
                parse_mode="Markdown",
                protect_content=True
            )
            await UserStates.SELECTING_LANGUAGE.set()

    except Exception as e:
        logging.error(f"Bot boshlashda xatolik: user_id={user_id}, error={e}")
        await message.answer(
            await get_message_async("uz", "error_occurred"),
            parse_mode="Markdown",
            protect_content=True
        )


@dp.message_handler(content_types=types.ContentTypes.TEXT, state="*")
async def handle_text_messages(message: types.Message, state: FSMContext):
    """Handle all text messages"""
    user_id = message.from_user.id
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"

    # Til sozlamalari tekshiruvi
    if await is_language_settings_text(message.text):
        await message.answer(
            await get_message_async(user_language, "select_new_language"),
            reply_markup=get_language_inline_keyboard(),
            parse_mode="Markdown",
            protect_content=True
        )
        await UserStates.SELECTING_LANGUAGE.set()
        logging.info(f"Til sozlamalari ochildi: user_id={user_id}")
        return

    # Bo'lim tanlash tekshiruvi
    section = await get_section_type_from_text(message.text)
    if section is not None:
        try:
            user = await user_db.select_user(telegram_id=user_id)
            if not user:
                await message.answer(
                    await get_message_async("uz", "error_occurred"),
                    parse_mode="Markdown",
                    protect_content=True
                )
                return

            user_language = user.get("language", "uz")
            is_allowed = user.get("is_allowed", False)
            is_admin = user.get("is_admin", False)

            if not (is_allowed or is_admin):
                await message.answer(
                    await get_message_async(user_language, "no_access"),
                    parse_mode="Markdown",
                    protect_content=True
                )
                return

            await user_db.update_last_active(telegram_id=user_id)

            items = []
            if section == "question":
                items = await sections_db.get_questions(language=user_language)
            elif section == "road_sign":
                items = await sections_db.get_road_signs(language=user_language)
            elif section == "truck_part":
                items = await sections_db.get_truck_parts(language=user_language)

            valid_items = [item for item in items if item and isinstance(item, dict)]
            if not valid_items:
                await message.answer(
                    await get_message_async(user_language, "no_data"),
                    parse_mode="Markdown",
                    protect_content=True
                )
                return

            items_per_page = 10
            page = 1
            start_idx = (page - 1) * items_per_page
            paginated_items = valid_items[start_idx:start_idx + items_per_page]

            await message.answer(
                await get_section_list_title(section, user_language),
                reply_markup=await get_section_items_keyboard(paginated_items, section, user_language, page,
                                                              len(valid_items)),
                parse_mode="Markdown",
                protect_content=True
            )
            logging.info(f"Bo'lim tanlandi: user_id={user_id}, section={section}")
            return

        except Exception as e:
            logging.error(f"Bo'lim tanlashda xatolik: user_id={user_id}, error={e}")
            await message.answer(
                await get_message_async(user_language, "error_occurred"),
                parse_mode="Markdown",
                protect_content=True
            )
            return

    # Boshqa xabarlar uchun
    current_state = await state.get_state()
    if current_state == UserStates.WAITING_FOR_PAYMENT.state:
        await message.answer(
            await get_message_async(user_language, "payment_required"),
            parse_mode="Markdown",
            protect_content=True
        )
    else:
        await message.answer(
            await get_message_async(user_language, "select_section"),
            reply_markup=await get_main_menu(user_language),
            parse_mode="Markdown",
            protect_content=True
        )
    logging.info(f"Kutilmagan xabar qayta ishlandi: user_id={user_id}, state={current_state}")


@dp.callback_query_handler(lambda c: c.data.startswith("lang_"), state=UserStates.SELECTING_LANGUAGE)
async def process_language_selection(callback_query: types.CallbackQuery, state: FSMContext):
    """Language selection callback handler"""
    user_id = callback_query.from_user.id
    lang = callback_query.data.split("_")[1]

    try:
        await user_db.update_user_language(telegram_id=user_id, language=lang)
        await user_db.update_last_active(telegram_id=user_id)
        await callback_query.message.delete()

        user = await user_db.select_user(telegram_id=user_id)
        is_allowed = user.get("is_allowed", False) if user else False
        is_admin = user.get("is_admin", False) if user else False

        await bot.send_message(
            user_id,
            await get_message_async(lang, "language_saved"),
            parse_mode="Markdown",
            protect_content=True
        )

        if is_admin or is_allowed:
            await bot.send_message(
                user_id,
                await get_message_async(lang, "success_message"),
                reply_markup=await get_main_menu(lang),
                parse_mode="Markdown",
                protect_content=True
            )
            await state.finish()
        else:
            await bot.send_message(
                user_id,
                await get_message_async(lang, "payment_required"),
                parse_mode="Markdown",
                protect_content=True
            )
            await UserStates.WAITING_FOR_PAYMENT.set()

        logging.info(f"Til tanlandi: user_id={user_id}, language={lang}")

    except Exception as e:
        logging.error(f"Til yangilashda xatolik: user_id={user_id}, error={e}")
        await callback_query.answer(await get_message_async("uz", "error_occurred"), show_alert=True)


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=UserStates.WAITING_FOR_PAYMENT)
async def handle_payment_photo(message: types.Message, state: FSMContext):
    """Payment photo handler"""
    user_id = message.from_user.id
    photo_file_id = message.photo[-1].file_id
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"

    try:
        pending_payment = await payment_db.get_user_pending_payment(telegram_id=user_id)
        if pending_payment:
            await message.answer(
                await get_message_async(user_language, "payment_already_pending"),
                parse_mode="Markdown",
                protect_content=True
            )
            return

        # Real vaqtda to'lov ma'lumotlarini olish
        payment_info = await payment_cache.get_payment_info()

        payment_id = await payment_db.add_payment(
            telegram_id=user_id,
            photo_file_id=photo_file_id,
            amount=payment_info['amount']
        )

        await message.answer(
            await get_message_async(user_language, "payment_received"),
            parse_mode="Markdown",
            protect_content=True
        )

        # Maxsus belgilarni ekranlash funksiyasi
        def escape_markdown_v2(text):
            """MarkdownV2 uchun maxsus belgilarni ekranlash"""
            special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            for char in special_chars:
                text = text.replace(char, f'\\{char}')
            return text

        # Ma'lumotlarni xavfsiz formatga o'tkazish
        username = message.from_user.username or message.from_user.full_name
        safe_username = escape_markdown_v2(username)
        safe_user_id = escape_markdown_v2(str(user_id))
        safe_amount = escape_markdown_v2(str(payment_info['amount']))

        # Vaqtni formatlash
        current_time = message.date.strftime("%Y-%m-%d %H:%M:%S")
        safe_time = escape_markdown_v2(current_time)

        admin_message = (
            f"🆕 *Yangi to'lov cheki\\!*\n\n"
            f"👤 *Foydalanuvchi ID:* `{safe_user_id}`\n"
            f"👤 *Username:* @{safe_username}\n"
            f"💰 *To'lov summasi:* ${safe_amount}\n"
            f"📅 *Vaqt:* {safe_time}\n\n"
            f"✅ *Tasdiqlash:* `/allow {safe_user_id}`\n"
            f"❌ *Rad qilish:* `/disallow {safe_user_id}`"
        )

        payment_keyboard = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("✅ Ruxsat Berish", callback_data=f"allow_{user_id}"),
            InlineKeyboardButton("❌ Rad Qilish", callback_data=f"disallow_{user_id}")
        )

        for admin_id in ADMINS:
            try:
                await bot.send_photo(
                    chat_id=admin_id,
                    photo=photo_file_id,
                    caption=admin_message,
                    reply_markup=payment_keyboard,
                    parse_mode="MarkdownV2"
                )
            except Exception as admin_error:
                logging.error(f"Admin {admin_id} ga xabar yuborishda xatolik: {admin_error}")
                # Zaxira xabar, Markdownsiz
                try:
                    await bot.send_photo(
                        chat_id=admin_id,
                        photo=photo_file_id,
                        caption=(
                            f"Yangi to'lov cheki!\n\n"
                            f"Foydalanuvchi ID: {user_id}\n"
                            f"Username: @{username}\n"
                            f"To'lov summasi: ${payment_info['amount']}\n"
                            f"Vaqt: {current_time}\n\n"
                            f"Tasdiqlash: /allow {user_id}\n"
                            f"Rad qilish: /disallow {user_id}"
                        ),
                        reply_markup=payment_keyboard
                    )
                except Exception as fallback_error:
                    logging.error(f"Zaxira xabar ham yuborilmadi: {fallback_error}")

        await state.finish()
        logging.info(f"To'lov yuborildi: user_id={user_id}, payment_id={payment_id}, amount=${payment_info['amount']}")

    except Exception as e:
        logging.error(f"To'lovni qayta ishlashda xatolik: user_id={user_id}, error={e}")
        await message.answer(
            await get_message_async(user_language, "error_occurred"),
            parse_mode="Markdown",
            protect_content=True
        )


@dp.callback_query_handler(lambda c: c.data.startswith("page_"))
async def handle_pagination(callback_query: types.CallbackQuery, state: FSMContext):
    """Pagination handler"""
    try:
        user_id = callback_query.from_user.id
        data_parts = callback_query.data.split("_")
        section = data_parts[1]
        page = int(data_parts[2])
        language = data_parts[3]

        items = []
        if section == "question":
            items = await sections_db.get_questions(language=language)
        elif section == "road_sign":
            items = await sections_db.get_road_signs(language=language)
        elif section == "truck_part":
            items = await sections_db.get_truck_parts(language=language)

        valid_items = [item for item in items if item and isinstance(item, dict)]
        items_per_page = 10
        start_idx = (page - 1) * items_per_page
        paginated_items = valid_items[start_idx:start_idx + items_per_page]

        await callback_query.message.edit_text(
            await get_section_list_title(section, language),
            reply_markup=await get_section_items_keyboard(paginated_items, section, language, page, len(valid_items)),
            parse_mode="Markdown"
        )
        await callback_query.answer()
        logging.info(f"Paginatsiya: user_id={user_id}, section={section}, page={page}")

    except Exception as e:
        logging.error(f"Paginatsiyada xatolik: user_id={user_id}, error={e}")
        await callback_query.answer(await get_message_async("uz", "error_occurred"), show_alert=True)


@dp.callback_query_handler(lambda c: c.data.startswith(("question_", "road_sign_", "truck_part_")))
async def handle_item_selection(callback_query: types.CallbackQuery, state: FSMContext):
    """Item selection handler"""
    try:
        user_id = callback_query.from_user.id
        callback_data = callback_query.data

        user = await user_db.select_user(telegram_id=user_id)
        if not user:
            await callback_query.answer(await get_message_async("uz", "error_occurred"), show_alert=True)
            return

        user_language = user.get("language", "uz")
        if not (user.get("is_allowed", False) or user.get("is_admin", False)):
            await callback_query.message.delete()
            await callback_query.answer(await get_message_async(user_language, "no_access"), show_alert=True)
            return

        section = None
        item_id = None
        try:
            if callback_data.startswith("question_"):
                section = "question"
                item_id = int(callback_data.replace("question_", ""))
            elif callback_data.startswith("road_sign_"):
                section = "road_sign"
                item_id = int(callback_data.replace("road_sign_", ""))
            elif callback_data.startswith("truck_part_"):
                section = "truck_part"
                item_id = int(callback_data.replace("truck_part_", ""))
        except ValueError:
            await callback_query.answer(await get_message_async(user_language, "error_occurred"), show_alert=True)
            return

        item = None
        if section == "question":
            item = await sections_db.get_question_by_id(item_id, language=user_language)
        elif section == "road_sign":
            item = await sections_db.get_road_sign_by_id(item_id, language=user_language)
        elif section == "truck_part":
            item = await sections_db.get_truck_part_by_id(item_id, language=user_language)

        if not item:
            await callback_query.answer(await get_message_async(user_language, "item_not_found"), show_alert=True)
            return

        await send_item_content(callback_query.message, item, section, user_language)
        await callback_query.answer()
        await user_db.update_last_active(telegram_id=user_id)
        logging.info(f"Element tanlandi: user_id={user_id}, section={section}, item_id={item_id}")

    except Exception as e:
        logging.error(f"Element tanlashda xatolik: user_id={user_id}, callback_data={callback_data}, error={e}")
        await callback_query.answer(await get_message_async(user_language, "error_occurred"), show_alert=True)


async def send_item_content(message: types.Message, item: dict, section: str, language: str):
    """Send item content based on section type"""
    try:
        # Maxsus belgilarni ekranlash funksiyasi
        def escape_markdown_v2(text: str) -> str:
            """MarkdownV2 uchun maxsus belgilarni ekranlash"""
            if not text or not isinstance(text, str):
                return ""
            # Nuqta (.) ni olib tashlash - bu maxsus belgi emas
            special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '!']
            for char in special_chars:
                text = text.replace(char, f'\\{char}')
            return text

        # Matnni chegaraga mos qisqartirish funksiyasi
        def limit_text(text: str, max_length: int) -> str:
            """Matnni berilgan uzunlikka qisqartirish"""
            if not text or not isinstance(text, str):
                return ""
            return text[:max_length] + "..." if len(text) > max_length else text

        # Maksimal uzunliklar
        max_caption_length = 1000  # Telegram caption uchun xavfsiz uzunlik
        max_message_length = 4000  # Telegram oddiy xabar uchun xavfsiz uzunlik

        # Matnni xavfsiz tarzda olish
        def safe_get(item: dict, key: str, default: str = "") -> str:
            value = item.get(key)
            return str(value) if value is not None else default

        # Xavfsiz media yuborish funksiyasi
        async def send_media_safely(media_type: str, file_id: str, caption: str = None):
            """Media ni xavfsiz yuborish"""
            try:
                if media_type == "photo":
                    await message.answer_photo(
                        photo=file_id,
                        caption=caption,
                        parse_mode="MarkdownV2" if caption else None,
                        protect_content=True
                    )
                elif media_type == "audio":
                    await message.answer_audio(
                        audio=file_id,
                        caption=caption,
                        parse_mode="MarkdownV2" if caption else None,
                        protect_content=True
                    )
                return True
            except Exception as e:
                logging.error(f"{media_type} yuborishda xatolik: {e}")
                return False

        # Matnni bo'laklarga bo'lib yuborish
        async def send_text_parts(text: str):
            """Uzun matnni bo'laklarga bo'lib yuborish"""
            for i in range(0, len(text), max_message_length):
                part = text[i:i + max_message_length]
                try:
                    await message.answer(
                        part,
                        parse_mode="MarkdownV2",
                        protect_content=True
                    )
                except Exception as e:
                    logging.error(f"Matn yuborishda xatolik: {e}")
                    # Fallback - oddiy matn sifatida yuborish
                    await message.answer(
                        part.replace('\\', ''),
                        protect_content=True
                    )

        if section == "question":
            question_text = safe_get(item, 'question')
            answer_text = safe_get(item, 'answer')
            display_id = safe_get(item, 'display_id', safe_get(item, 'id', 'Noma\'lum'))

            logging.info(f"Raw question text: {question_text}")
            logging.info(f"Raw answer text: {answer_text}")
            logging.info(f"Display ID: {display_id}")

            # Faqat user content ni ekranlash
            question_text = escape_markdown_v2(question_text)
            answer_text = escape_markdown_v2(answer_text)
            display_id = escape_markdown_v2(str(display_id))

            # Lokalizatsiya matnlarini ekranlamaslik
            question_label = await get_message_async(language, 'question_label')
            answer_label = await get_message_async(language, 'answer_label')

            logging.info(f"Escaped question text: {question_text}")
            logging.info(f"Escaped answer text: {answer_text}")

            full_text = f"❓ {question_label} \\#{display_id}:\n{question_text}\n\n"
            full_text += f"✅ {answer_label}:\n{answer_text}"
            logging.info(f"Question full text: {full_text}")

            # Audio mavjud bo'lsa, yuborish
            if item.get("audio_file_id"):
                audio_caption = await get_message_async(language, "audio_caption")
                await send_media_safely("audio", item["audio_file_id"], audio_caption)

            # Rasm mavjud bo'lsa
            if item.get("image_file_id"):
                caption_text = limit_text(full_text, max_caption_length)
                success = await send_media_safely("photo", item["image_file_id"], caption_text)

                if success:
                    # Agar matn uzun bo'lsa, qolgan qismini alohida yuborish
                    if len(full_text) > max_caption_length:
                        remaining_text = full_text[max_caption_length:]
                        await send_text_parts(remaining_text)
                    return
                else:
                    # Rasm yuborib bo'lmasa, faqat matn yuborish
                    logging.warning("Rasm yuborib bo'lmadi, faqat matn yuboriladi")

            # Faqat matn yuborish
            logging.info(f"Sending question text only: {full_text}")
            await send_text_parts(full_text)

        elif section == "road_sign":
            sign_name = safe_get(item, 'name')
            sign_description = safe_get(item, 'description')

            logging.info(f"Raw road sign name: {sign_name}")
            logging.info(f"Raw road sign description: {sign_description}")

            sign_name = escape_markdown_v2(sign_name)
            sign_description = escape_markdown_v2(sign_description)

            # Yo'l belgisi uchun to'liq matnni yaratish
            road_sign_label = await get_message_async(language, 'road_sign')
            full_text = f"🚦 {road_sign_label}: {sign_name}"

            if sign_description and sign_description.strip():
                full_text += f"\n\n📝 Info:\n{sign_description}"

            logging.info(f"Road sign full text: {full_text}")

            # Rasm mavjud bo'lsa
            if item.get("image_file_id"):
                await send_media_safely("photo", item["image_file_id"])

            # Matn yuborish
            if full_text and (sign_name.strip() or sign_description.strip()):
                await send_text_parts(full_text)

        elif section == "truck_part":
            part_name = safe_get(item, 'name')
            part_description = safe_get(item, 'description')

            logging.info(f"Raw truck part name: {part_name}")
            logging.info(f"Raw truck part description: {part_description}")

            part_name = escape_markdown_v2(part_name)
            part_description = escape_markdown_v2(part_description)

            # Truck ehtiyot qismi uchun to'liq matnni yaratish
            truck_part_label = await get_message_async(language, 'truck_part')
            full_text = f"🚚 {truck_part_label}: {part_name}"

            if part_description and part_description.strip():
                full_text += f"\n\n📝 Info:\n{part_description}"

            logging.info(f"Truck part full text: {full_text}")

            # Rasm mavjud bo'lsa
            if item.get("image_file_id"):
                await send_media_safely("photo", item["image_file_id"])

            # Matn yuborish
            if full_text and (part_name.strip() or part_description.strip()):
                await send_text_parts(full_text)

    except Exception as e:
        logging.error(f"Element mazmunini yuborishda xatolik: {e}, section={section}, item={item}")
        try:
            error_message = await get_message_async(language, "error_occurred")
            await message.answer(
                error_message,
                protect_content=True
            )
        except Exception as fallback_error:
            logging.error(f"Xato xabarini yuborishda xatolik: {fallback_error}")
            await message.answer(
                "Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
                protect_content=True
            )


@dp.callback_query_handler(lambda c: c.data == "back_to_menu")
async def handle_back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Back to menu handler"""
    user_id = callback_query.from_user.id

    try:
        user = await user_db.select_user(telegram_id=user_id)
        if not user:
            await callback_query.answer(await get_message_async("uz", "error_occurred"), show_alert=True)
            return

        user_language = user.get("language", "uz")

        # Xabarni o'chirish
        try:
            await callback_query.message.delete()
        except Exception as delete_error:
            logging.warning(f"Xabarni o'chirishda xatolik: {delete_error}")

        await bot.send_message(
            user_id,
            await get_message_async(user_language, "select_section"),
            reply_markup=await get_main_menu(user_language),
            parse_mode="Markdown",
            protect_content=True
        )
        await callback_query.answer()
        logging.info(f"Orqaga menyuga qaytildi: user_id={user_id}")

    except Exception as e:
        logging.error(f"Orqaga menyuga qaytishda xatolik: user_id={user_id}, error={e}")
        try:
            await callback_query.answer(await get_message_async("uz", "error_occurred"), show_alert=True)
        except Exception as callback_error:
            logging.error(f"Callback javob berishda xatolik: {callback_error}")


@dp.callback_query_handler(lambda c: c.data.startswith(("allow_", "disallow_")))
async def handle_admin_payment_decision(callback_query: types.CallbackQuery, state: FSMContext):
    """Admin payment decision handler"""
    admin_id = callback_query.from_user.id
    target_user_id = None

    try:
        if admin_id not in ADMINS:
            await callback_query.answer("❌ Ruxsat yo'q!", show_alert=True)
            return

        # Data parsing
        try:
            action, target_user_id = callback_query.data.split("_")
            target_user_id = int(target_user_id)
        except (ValueError, IndexError) as parse_error:
            logging.error(f"Callback data parsing xatolik: {parse_error}")
            await callback_query.answer("❌ Noto'g'ri ma'lumot!", show_alert=True)
            return

        # Payment check
        payment = await payment_db.get_user_pending_payment(telegram_id=target_user_id)
        if not payment:
            await callback_query.answer("❌ To'lov topilmadi!", show_alert=True)
            return

        # User check
        user = await user_db.select_user(telegram_id=target_user_id)
        if not user:
            await callback_query.answer("❌ Foydalanuvchi topilmadi!", show_alert=True)
            return

        user_language = user.get("language", "uz")

        if action == "allow":
            # Payment approval
            await user_db.update_user_access(telegram_id=target_user_id, is_allowed=True)
            await payment_db.update_payment_status(payment_id=payment['id'], status='approved')

            # Notify user
            try:
                await bot.send_message(
                    target_user_id,
                    await get_message_async(user_language, "success_message"),
                    reply_markup=await get_main_menu(user_language),
                    parse_mode="Markdown",
                    protect_content=True
                )
            except Exception as user_notify_error:
                logging.error(f"Foydalanuvchi {target_user_id} ga xabar yuborishda xatolik: {user_notify_error}")

            # Update admin message
            try:
                await callback_query.message.edit_caption(
                    f"✅ *TASDIQLANDI*\n\n{callback_query.message.caption}",
                    parse_mode="Markdown"
                )
            except Exception as edit_error:
                logging.error(f"Admin xabarini yangilashda xatolik: {edit_error}")

            await callback_query.answer("✅ To'lov tasdiqlandi!", show_alert=True)

        elif action == "disallow":
            # Payment rejection
            await payment_db.update_payment_status(payment_id=payment['id'], status='rejected')

            # Notify user
            try:
                await bot.send_message(
                    target_user_id,
                    await get_message_async(user_language, "payment_rejected"),
                    parse_mode="Markdown",
                    protect_content=True
                )
            except Exception as user_notify_error:
                logging.error(f"Foydalanuvchi {target_user_id} ga xabar yuborishda xatolik: {user_notify_error}")

            # Update admin message
            try:
                await callback_query.message.edit_caption(
                    f"❌ *RAD QILINDI*\n\n{callback_query.message.caption}",
                    parse_mode="Markdown"
                )
            except Exception as edit_error:
                logging.error(f"Admin xabarini yangilashda xatolik: {edit_error}")

            await callback_query.answer("❌ To'lov rad qilindi!", show_alert=True)

        logging.info(f"To'lov qarori: admin_id={admin_id}, user_id={target_user_id}, action={action}")

    except Exception as e:
        logging.error(f"To'lov qarorida xatolik: admin_id={admin_id}, user_id={target_user_id}, error={e}")
        try:
            await callback_query.answer("❌ Xatolik yuz berdi!", show_alert=True)
        except Exception as callback_error:
            logging.error(f"Callback javob berishda xatolik: {callback_error}")


@dp.message_handler(commands=['allow'], user_id=ADMINS)
async def allow_user_command(message: types.Message):
    """Allow user command"""
    admin_id = message.from_user.id
    target_user_id = None

    try:
        args = message.text.split()
        if len(args) != 2:
            await message.answer("❌ Foydalanish: /allow <user_id>")
            return

        try:
            target_user_id = int(args[1])
        except ValueError:
            await message.answer("❌ Noto'g'ri user_id formatı!")
            return

        # Update user access
        await user_db.update_user_access(telegram_id=target_user_id, is_allowed=True)

        # Notify user
        user = await user_db.select_user(telegram_id=target_user_id)
        if user:
            user_language = user.get("language", "uz")
            try:
                await bot.send_message(
                    target_user_id,
                    await get_message_async(user_language, "success_message"),
                    reply_markup=await get_main_menu(user_language),
                    parse_mode="Markdown",
                    protect_content=True
                )
            except Exception as notify_error:
                logging.error(f"Foydalanuvchi {target_user_id} ga xabar yuborishda xatolik: {notify_error}")

        await message.answer(f"✅ Foydalanuvchi {target_user_id} ga ruxsat berildi!")
        logging.info(f"Ruxsat berildi: admin_id={admin_id}, user_id={target_user_id}")

    except Exception as e:
        logging.error(f"Ruxsat berishda xatolik: admin_id={admin_id}, user_id={target_user_id}, error={e}")
        await message.answer("❌ Xatolik yuz berdi!")


@dp.message_handler(commands=['disallow'], user_id=ADMINS)
async def disallow_user_command(message: types.Message):
    """Disallow user command"""
    admin_id = message.from_user.id
    target_user_id = None

    try:
        args = message.text.split()
        if len(args) != 2:
            await message.answer("❌ Foydalanish: /disallow <user_id>")
            return

        try:
            target_user_id = int(args[1])
        except ValueError:
            await message.answer("❌ Noto'g'ri user_id formatı!")
            return

        await user_db.update_user_access(telegram_id=target_user_id, is_allowed=False)
        await message.answer(f"❌ Foydalanuvchi {target_user_id} dan ruxsat olib tashlandi!")
        logging.info(f"Ruxsat olindi: admin_id={admin_id}, user_id={target_user_id}")

    except Exception as e:
        logging.error(f"Ruxsat olib tashlashda xatolik: admin_id={admin_id}, user_id={target_user_id}, error={e}")
        await message.answer("❌ Xatolik yuz berdi!")


@dp.message_handler(commands=['reload_config'], user_id=ADMINS)
async def reload_config_command(message: types.Message):
    """Reload payment configuration"""
    admin_id = message.from_user.id

    try:
        # Clear cache
        payment_cache.clear_cache()

        # Get updated payment info
        payment_info = await payment_cache.get_payment_info()

        if not payment_info:
            await message.answer("❌ To'lov ma'lumotlarini olishda xatolik!")
            return

        config_message = (
            f"🔄 *Konfiguratsiya yangilandi!*\n\n"
            f"💰 *Yangi to'lov summasi:* ${payment_info['amount']}\n"
            f"💳 *Yangi karta raqami:* `{payment_info['card']}`\n"
            f"👤 *Yangi karta egasi:* {payment_info['owner']}"
        )

        await message.answer(config_message, parse_mode="Markdown")
        logging.info(f"Config qayta yuklandi: admin_id={admin_id}")

    except Exception as e:
        logging.error(f"Config qayta yuklashda xatolik: admin_id={admin_id}, error={e}")
        await message.answer("❌ Xatolik yuz berdi!")


@dp.message_handler(content_types=types.ContentTypes.ANY, state="*")
async def handle_unexpected_message(message: types.Message, state: FSMContext):
    """Handle unexpected messages"""
    user_id = message.from_user.id

    try:
        # Get user language
        user = await user_db.select_user(telegram_id=user_id)
        user_language = user.get("language", "uz") if user else "uz"

        # Skip text messages - they are handled elsewhere
        if message.content_type == types.ContentType.TEXT:
            return

        # Block forwarded messages
        if message.forward_from or message.forward_from_chat:
            await message.answer(
                await get_message_async(user_language, "forward_prohibited"),
                parse_mode="Markdown",
                protect_content=True
            )
            logging.info(f"Forward qilingan xabar bloklandi: user_id={user_id}")
            return

        # Handle based on current state
        current_state = await state.get_state()
        if current_state == UserStates.WAITING_FOR_PAYMENT.state:
            await message.answer(
                await get_message_async(user_language, "payment_required"),
                parse_mode="Markdown",
                protect_content=True
            )
        else:
            await message.answer(
                await get_message_async(user_language, "select_section"),
                reply_markup=await get_main_menu(user_language),
                parse_mode="Markdown",
                protect_content=True
            )

        logging.info(
            f"Kutilmagan xabar qayta ishlandi: user_id={user_id}, content_type={message.content_type}, state={current_state}")

    except Exception as e:
        logging.error(f"Kutilmagan xabarni qayta ishlashda xatolik: user_id={user_id}, error={e}")
        try:
            await message.answer(
                await get_message_async("uz", "error_occurred"),
                parse_mode="Markdown",
                protect_content=True
            )
        except Exception as send_error:
            logging.error(f"Xato xabarini yuborishda xatolik: {send_error}")


@dp.message_handler(commands=['cancel'], state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    """Cancel command to reset state and return to main menu"""
    user_id = message.from_user.id

    try:
        # Get user info
        user = await user_db.select_user(telegram_id=user_id)
        user_language = user.get("language", "uz") if user else "uz"

        # Reset the current state
        await state.finish()

        # Update last active timestamp
        if user:
            await user_db.update_last_active(telegram_id=user_id)

        # Send main menu
        await message.answer(
            await get_message_async(user_language, "select_section"),
            reply_markup=await get_main_menu(user_language),
            parse_mode="Markdown",
            protect_content=True
        )

        logging.info(f"Cancel command executed: user_id={user_id}, language={user_language}")

    except Exception as e:
        logging.error(f"Cancel command xatolik: user_id={user_id}, error={e}")
        try:
            await message.answer(
                await get_message_async("uz", "error_occurred"),
                parse_mode="Markdown",
                protect_content=True
            )
        except Exception as send_error:
            logging.error(f"Xato xabarini yuborishda xatolik: {send_error}")