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
        """Kesh orqali to‘lov ma'lumotlarini olish"""
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
            from data.config import PAYMENT_AMOUNT, PAYMENT_CARD, PAYMENT_OWNER

            self._cache = {
                'amount': float(PAYMENT_AMOUNT),
                'card': PAYMENT_CARD,
                'owner': PAYMENT_OWNER
            }
            self._last_updated = time.time()
        except Exception as e:
            logging.error(f"To‘lov keshini yangilashda xatolik: {e}")
            self._cache = {
                'amount': 10.00,  # Fallback qiymat
                'card': "9860 1234 5678 9012",
                'owner': "FATTOYEV ABDUFATTOH"
            }

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
    return {
        "uz": {
            "welcome": "🌟 *Xush kelibsiz!* 🌟\nIltimos, o‘zingiz uchun mos tilni tanlang 👇",
            "questions_answers": "📝 Savol va Javoblar",
            "road_signs": "🚦 Yo‘l Belgilari",
            "truck_parts": "🚚 Truck Ehtiyot Qismlari",
            "language_settings": "⚙️ Til Sozlamalari",
            "success_message": "✅ *Tabriklaymiz!* 🎉 Botdan foydalanishingiz mumkin! 🚀",
            "payment_required": f"💰 Botdan foydalanish uchun ${payment_info['amount']} to‘lov qiling va chekni yuboring 📸\n\n"
                               f"💳 *Karta raqami:* `{payment_info['card']}`\n"
                               f"👤 *Karta egasi:* {payment_info['owner']}",
            "select_new_language": "🌐 *Yangi tilni tanlang:* 👇",
            "language_saved": "✅ *Til saqlandi!* 🌟 Endi botni o‘zingiz uchun sozlang!",
            "payment_received": "📩 *Chek qabul qilindi!* ✅ Admin tasdiqlashini kuting ⏳",
            "payment_already_pending": "⚠️ *Diqqat!* Sizning oldingi chekingiz hali ko‘rib chiqilmoqda. Iltimos, kuting! ⏳",
            "no_access": "❌ *Ruxsat yo‘q!* 💡 Botdan foydalanish uchun to‘lov qiling.",
            "no_data": "⚠️ *Diqqat!* Bu bo‘limda hozircha ma‘lumot yo‘q. Keling, keyinroq urinib ko‘ramiz! 😊",
            "select_section": "📋 *Iltimos, menyudan bo‘lim tanlang:* 👇",
            "error_occurred": "🚫 *Xatolik yuz berdi!* 😔 Iltimos, qayta urinib ko‘ring.",
            "item_not_found": "🔍 *Element topilmadi!* Iltimos, boshqa elementni tanlang.",
            "forward_prohibited": "⚠️ *Forward taqiqlangan!* 🚫 Xabarni qayta yubormang.",
            "previous": "⬅️ Oldingi",
            "next": "Keyingi ➡️",
            "question": "📝 Savol",
            "road_sign": "🚦 Yo‘l Belgisi",
            "truck_part": "🚚 Truck Zapchasti",
            "questions_list": "📚 *Savol va Javoblar Ro‘yxati:*",
            "road_signs_list": "🚦 *Yo‘l Belgilari Ro‘yxati:*",
            "truck_parts_list": "🚚 *Truck Zapchastlari Ro‘yxati:*",
            "question_label": "📌 *Savol:*",
            "answer_label": "💡 *Javob:*",
            "audio_caption": "🎵 *Savol Audiosi*",
            "back_to_menu": "🔙 Orqaga",
            "payment_rejected": "❌ *Kechirasiz, to‘lovingiz rad etildi! Iltimos, qayta urinib ko‘ring.*"
        },
        "ru": {
            "welcome": "🌟 *Добро пожаловать!* 🌟\nПожалуйста, выберите язык 👇",
            "questions_answers": "📝 Вопросы и ответы",
            "road_signs": "🚦 Дорожные знаки",
            "truck_parts": "🚚 Запчасти для грузовиков",
            "language_settings": "⚙️ Настройки языка",
            "success_message": "✅ *Поздравляем!* 🎉 Вы можете использовать бота! 🚀",
            "payment_required": f"💰 Оплатите ${payment_info['amount']} для использования бота и отправьте чек 📸\n\n"
                               f"💳 *Номер карты:* `{payment_info['card']}`\n"
                               f"👤 *Владелец карты:* {payment_info['owner']}",
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
                               f"💳 *Número de tarjeta:* `{payment_info['card']}`\n"
                               f"👤 *Titular de la tarjeta:* {payment_info['owner']}",
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
            content = item.get("question", item.get("description", "Kontent yo‘q"))
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


# @dp.message_handler(content_types=types.ContentTypes.TEXT)
# async def handle_language_settings(message: types.Message, state: FSMContext):
#     """Language settings handler"""
#     user_id = message.from_user.id
#     user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"
#
#     # Check if the message text corresponds to the language settings button
#     if await is_language_settings_text(message.text):
#         await message.answer(
#             await get_message_async(user_language, "select_new_language"),
#             reply_markup=get_language_inline_keyboard(),
#             parse_mode="Markdown",
#             protect_content=True
#         )
#         await UserStates.SELECTING_LANGUAGE.set()
#         logging.info(f"Til sozlamalari ochildi: user_id={user_id}")

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



# @dp.message_handler(content_types=types.ContentTypes.TEXT)
# async def handle_section_selection(message: types.Message, state: FSMContext):
#     """Section selection handler"""
#     user_id = message.from_user.id
#     section = await get_section_type_from_text(message.text)
#
#     if section is None:
#         return  # If not a section selection, skip processing
#
#     try:
#         user = await user_db.select_user(telegram_id=user_id)
#         if not user:
#             await message.answer(
#                 await get_message_async("uz", "error_occurred"),
#                 parse_mode="Markdown",
#                 protect_content=True
#             )
#             return
#
#         user_language = user.get("language", "uz")
#         is_allowed = user.get("is_allowed", False)
#         is_admin = user.get("is_admin", False)
#
#         if not (is_allowed or is_admin):
#             await message.answer(
#                 await get_message_async(user_language, "no_access"),
#                 parse_mode="Markdown",
#                 protect_content=True
#             )
#             return
#
#         await user_db.update_last_active(telegram_id=user_id)
#
#         items = []
#         if section == "question":
#             items = await sections_db.get_questions(language=user_language)
#         elif section == "road_sign":
#             items = await sections_db.get_road_signs(language=user_language)
#         elif section == "truck_part":
#             items = await sections_db.get_truck_parts(language=user_language)
#
#         valid_items = [item for item in items if item and isinstance(item, dict)]
#         if not valid_items:
#             await message.answer(
#                 await get_message_async(user_language, "no_data"),
#                 parse_mode="Markdown",
#                 protect_content=True
#             )
#             return
#
#         items_per_page = 10
#         page = 1
#         start_idx = (page - 1) * items_per_page
#         paginated_items = valid_items[start_idx:start_idx + items_per_page]
#
#         await message.answer(
#             await get_section_list_title(section, user_language),
#             reply_markup=await get_section_items_keyboard(paginated_items, section, user_language, page,
#                                                           len(valid_items)),
#             parse_mode="Markdown",
#             protect_content=True
#         )
#         logging.info(f"Bo‘lim tanlandi: user_id={user_id}, section={section}")
#
#     except Exception as e:
#         logging.error(f"Bo‘lim tanlashda xatolik: user_id={user_id}, error={e}")
#         await message.answer(
#             await get_message_async(user_language, "error_occurred"),
#             parse_mode="Markdown",
#             protect_content=True
#         )

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
        back_keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(await get_message_async(language, "back_to_menu"), callback_data="back_to_menu")
        )

        if section == "question":
            question_text = f"{await get_message_async(language, 'question_label')} {item.get('question', 'Savol yo‘q')}\n\n"
            question_text += f"{await get_message_async(language, 'answer_label')} {item.get('answer', 'Javob yo‘q')}"

            if item.get("audio_file_id"):
                try:
                    await message.answer_audio(
                        audio=item["audio_file_id"],
                        caption=await get_message_async(language, "audio_caption"),
                        parse_mode="Markdown",
                        protect_content=True
                    )
                except Exception as audio_error:
                    logging.error(f"Audio yuborishda xatolik: {audio_error}")

            if item.get("image_file_id"):
                try:
                    await message.answer_photo(
                        photo=item["image_file_id"],
                        caption=question_text,
                        reply_markup=back_keyboard,
                        parse_mode="Markdown",
                        protect_content=True
                    )
                    return
                except Exception as photo_error:
                    logging.error(f"Rasm yuborishda xatolik: {photo_error}")

            await message.answer(
                question_text,
                reply_markup=back_keyboard,
                parse_mode="Markdown",
                protect_content=True
            )

        elif section == "road_sign":
            sign_text = f"{await get_message_async(language, 'road_sign')}: {item.get('name', 'Nomi yo‘q')}\n\n"
            sign_text += f"{item.get('description', 'Tavsif yo‘q')}"

            if item.get("image_file_id"):
                try:
                    await message.answer_photo(
                        photo=item["image_file_id"],
                        caption=sign_text,
                        reply_markup=back_keyboard,
                        parse_mode="Markdown",
                        protect_content=True
                    )
                    return
                except Exception as photo_error:
                    logging.error(f"Rasm yuborishda xatolik: {photo_error}")

            await message.answer(
                sign_text,
                reply_markup=back_keyboard,
                parse_mode="Markdown",
                protect_content=True
            )

        elif section == "truck_part":
            part_text = f"{await get_message_async(language, 'truck_part')}: {item.get('name', 'Nomi yo‘q')}\n\n"
            part_text += f"{item.get('description', 'Tavsif yo‘q')}"
            if item.get("price"):
                part_text += f"\n\n💰 *Narx:* ${item['price']}"

            if item.get("image_file_id"):
                try:
                    await message.answer_photo(
                        photo=item["image_file_id"],
                        caption=part_text,
                        reply_markup=back_keyboard,
                        parse_mode="Markdown",
                        protect_content=True
                    )
                    return
                except Exception as photo_error:
                    logging.error(f"Rasm yuborishda xatolik: {photo_error}")

            await message.answer(
                part_text,
                reply_markup=back_keyboard,
                parse_mode="Markdown",
                protect_content=True
            )

    except Exception as e:
        logging.error(f"Element mazmunini yuborishda xatolik: {e}")
        await message.answer(
            await get_message_async(language, "error_occurred"),
            parse_mode="Markdown",
            protect_content=True
        )

@dp.callback_query_handler(lambda c: c.data == "back_to_menu")
async def handle_back_to_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """Back to menu handler"""
    try:
        user_id = callback_query.from_user.id
        user = await user_db.select_user(telegram_id=user_id)

        if not user:
            await callback_query.answer(await get_message_async("uz", "error_occurred"), show_alert=True)
            return

        user_language = user.get("language", "uz")
        await callback_query.message.delete()

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
        await callback_query.answer(await get_message_async("uz", "error_occurred"), show_alert=True)

@dp.callback_query_handler(lambda c: c.data.startswith(("allow_", "disallow_")))
async def handle_admin_payment_decision(callback_query: types.CallbackQuery, state: FSMContext):
    """Admin payment decision handler"""
    try:
        admin_id = callback_query.from_user.id
        if admin_id not in ADMINS:
            await callback_query.answer("❌ Ruxsat yo‘q!", show_alert=True)
            return

        action, target_user_id = callback_query.data.split("_")
        target_user_id = int(target_user_id)

        payment = await payment_db.get_user_pending_payment(telegram_id=target_user_id)
        if not payment:
            await callback_query.answer("❌ To‘lov topilmadi!", show_alert=True)
            return

        user = await user_db.select_user(telegram_id=target_user_id)
        if not user:
            await callback_query.answer("❌ Foydalanuvchi topilmadi!", show_alert=True)
            return

        user_language = user.get("language", "uz")

        if action == "allow":
            await user_db.update_user_access(telegram_id=target_user_id, is_allowed=True)
            await payment_db.update_payment_status(payment_id=payment['id'], status='approved')

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

            await callback_query.message.edit_caption(
                f"✅ *TASDIQLANDI*\n\n{callback_query.message.caption}",
                parse_mode="Markdown"
            )
            await callback_query.answer("✅ To‘lov tasdiqlandi!", show_alert=True)

        elif action == "disallow":
            await payment_db.update_payment_status(payment_id=payment['id'], status='rejected')

            try:
                await bot.send_message(
                    target_user_id,
                    await get_message_async(user_language, "payment_rejected"),
                    parse_mode="Markdown",
                    protect_content=True
                )
            except Exception as user_notify_error:
                logging.error(f"Foydalanuvchi {target_user_id} ga xabar yuborishda xatolik: {user_notify_error}")

            await callback_query.message.edit_caption(
                f"❌ *RAD QILINDI*\n\n{callback_query.message.caption}",
                parse_mode="Markdown"
            )
            await callback_query.answer("❌ To‘lov rad qilindi!", show_alert=True)

        logging.info(f"To‘lov qarori: admin_id={admin_id}, user_id={target_user_id}, action={action}")

    except Exception as e:
        logging.error(f"To‘lov qarorida xatolik: admin_id={admin_id}, error={e}")
        await callback_query.answer(await get_message_async("uz", "error_occurred"), show_alert=True)

@dp.message_handler(commands=['allow'], user_id=ADMINS)
async def allow_user_command(message: types.Message):
    """Allow user command"""
    try:
        args = message.text.split()
        if len(args) != 2:
            await message.answer("❌ Foydalanish: /allow <user_id>")
            return

        user_id = int(args[1])
        await user_db.update_user_access(telegram_id=user_id, is_allowed=True)

        user = await user_db.select_user(telegram_id=user_id)
        if user:
            user_language = user.get("language", "uz")
            try:
                await bot.send_message(
                    user_id,
                    await get_message_async(user_language, "success_message"),
                    reply_markup=await get_main_menu(user_language),
                    parse_mode="Markdown",
                    protect_content=True
                )
            except Exception as notify_error:
                logging.error(f"Foydalanuvchi {user_id} ga xabar yuborishda xatolik: {notify_error}")

        await message.answer(f"✅ Foydalanuvchi {user_id} ga ruxsat berildi!")
        logging.info(f"Ruxsat berildi: user_id={user_id}")

    except Exception as e:
        logging.error(f"Ruxsat berishda xatolik: error={e}")
        await message.answer("❌ Xatolik yuz berdi!")

@dp.message_handler(commands=['disallow'], user_id=ADMINS)
async def disallow_user_command(message: types.Message):
    """Disallow user command"""
    try:
        args = message.text.split()
        if len(args) != 2:
            await message.answer("❌ Foydalanish: /disallow <user_id>")
            return

        user_id = int(args[1])
        await user_db.update_user_access(telegram_id=user_id, is_allowed=False)
        await message.answer(f"❌ Foydalanuvchi {user_id} dan ruxsat olib tashlandi!")
        logging.info(f"Ruxsat olindi: user_id={user_id}")

    except Exception as e:
        logging.error(f"Ruxsat olib tashlashda xatolik: error={e}")
        await message.answer("❌ Xatolik yuz berdi!")

@dp.message_handler(commands=['reload_config'], user_id=ADMINS)
async def reload_config_command(message: types.Message):
    """Reload payment configuration"""
    try:
        payment_cache.clear_cache()  # Keshni tozalash
        payment_info = await payment_cache.get_payment_info()

        config_message = (
            f"🔄 *Konfiguratsiya yangilandi!*\n\n"
            f"💰 *Yangi to‘lov summasi:* ${payment_info['amount']}\n"
            f"💳 *Yangi karta raqami:* `{payment_info['card']}`\n"
            f"👤 *Yangi karta egasi:* {payment_info['owner']}"
        )

        await message.answer(config_message, parse_mode="Markdown")
        logging.info(f"Config qayta yuklandi: admin_id={message.from_user.id}")

    except Exception as e:
        logging.error(f"Config qayta yuklashda xatolik: error={e}")
        await message.answer("❌ Xatolik yuz berdi!")


@dp.message_handler(content_types=types.ContentTypes.ANY, state="*")
async def handle_unexpected_message(message: types.Message, state: FSMContext):
    """Handle unexpected messages"""
    user_id = message.from_user.id
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"

    try:
        # Agar bu text message bo'lsa, handle_text_messages funksiyasi ishlatiladi
        if message.content_type == types.ContentType.TEXT:
            return

        if message.forward_from or message.forward_from_chat:
            await message.answer(
                await get_message_async(user_language, "forward_prohibited"),
                parse_mode="Markdown",
                protect_content=True
            )
            logging.info(f"Forward qilingan xabar bloklandi: user_id={user_id}")
            return

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

    except Exception as e:
        logging.error(f"Kutilmagan xabarni qayta ishlashda xatolik: user_id={user_id}, error={e}")
        await message.answer(
            await get_message_async(user_language, "error_occurred"),
            parse_mode="Markdown",
            protect_content=True
        )


@dp.message_handler(commands=['cancel'], state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    """Cancel command to reset state and return to main menu"""
    user_id = message.from_user.id
    try:
        user = await user_db.select_user(telegram_id=user_id)
        user_language = user.get("language", "uz") if user else "uz"

        # Reset the current state
        await state.finish()

        # Update last active timestamp
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
        logging.error(f"Error in cancel command: user_id={user_id}, error={e}")
        await message.answer(
            await get_message_async("uz", "error_occurred"),
            parse_mode="Markdown",
            protect_content=True
        )