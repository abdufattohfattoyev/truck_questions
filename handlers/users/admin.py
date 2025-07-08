from aiogram import types
from aiogram.dispatcher.filters import Filter
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot, user_db, sections_db, payment_db
from data.config import ADMINS, PAYMENT_AMOUNT
import logging
import os

logging.basicConfig(level=logging.INFO)

# To'lov summasi (standart qiymat, agar config'da bo'lmasa)
PAYMENT_AMOUNT = PAYMENT_AMOUNT if 'PAYMENT_AMOUNT' in globals() else 10.00


# States class
class UserStates(StatesGroup):
    SELECTING_LANGUAGE = State()
    WAITING_FOR_PAYMENT = State()


# Admin States
class AdminStates(StatesGroup):
    SELECT_SECTION = State()
    SELECT_LANGUAGE = State()
    ADD_QUESTION_TEXT = State()
    ADD_QUESTION_ANSWER = State()
    ADD_QUESTION_AUDIO = State()
    ADD_ROAD_SIGN_IMAGE = State()
    ADD_ROAD_SIGN_DESCRIPTION = State()
    ADD_TRUCK_PART_IMAGE = State()
    ADD_TRUCK_PART_DESCRIPTION = State()
    DELETE_SELECT_LANGUAGE = State()
    DELETE_SELECT_SECTION = State()
    DELETE_SELECT_ITEM = State()
    DELETE_CONFIRM = State()
    SET_PAYMENT_AMOUNT = State()


# Admin Filter
class AdminFilter(Filter):
    async def check(self, message: types.Message):
        return await user_db.check_if_admin(message.from_user.id)


# Super Admin Filter
class SuperAdminFilter(Filter):
    async def check(self, message: types.Message):
        return str(message.from_user.id) in ADMINS


# Enhanced localization messages
MESSAGES = {
    "uz": {
        "welcome": "🌟 *Xush kelibsiz!* 🌟\nIltimos, o'zingiz uchun mos tilni tanlang 👇",
        "questions_answers": "📝 Savol va Javoblar",
        "road_signs": "🚦 Yo'l Belgilari",
        "truck_parts": "🚚 Truck Zapchastlari",
        "language_settings": "⚙️ Til Sozlamalari",
        "success_message": "✅ *Tabriklaymiz!* 🎉 Botdan foydalanishingiz mumkin! 🚀",
        "payment_required": "💰 Botdan foydalanish uchun to'lov qiling va chekni yuboring 📸",
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
        "next": "➡️ Keyingi",
        "question": "📝 Savol",
        "road_sign": "🚦 Yo'l Belgisi",
        "truck_part": "🚚 Truck Zapchasti",
        "questions_list": "📚 *Savol va Javoblar Ro'yxati:*",
        "road_signs_list": "🚦 *Yo'l Belgilari Ro'yxati:*",
        "truck_parts_list": "🚚 *Truck Zapchastlari Ro'yxati:*",
        "question_label": "📌 *Savol:*",
        "answer_label": "💡 *Javob:*",
        "audio_caption": "🎵 *Savol Audiosi*",
        "back_to_menu": "🔙 Orqaga",
        # Admin xabarlar
        "admin_welcome": f"👑 *Admin paneliga xush kelibsiz!* 🌟\n💰 *Joriy to'lov summasi:* ${PAYMENT_AMOUNT}\nTanlang:",
        "add_question": "📝 *Savol qo'shish jarayoni boshlandi!*",
        "add_road_sign": "🚦 *Yo'l belgisi qo'shish jarayoni boshlandi!*",
        "add_truck_part": "🚚 *Truck zapchasti qo'shish jarayoni boshlandi!*",
        "delete_welcome": "🗑️ *O'chirish uchun tilni tanlang:*",
        "delete_section": "📋 *O'chirish uchun bo'limni tanlang:*",
        "delete_item": "🔍 *O'chirish uchun elementni tanlang:*",
        "confirm_delete": "⚠️ *O'chirishni tasdiqlaysizmi?*",
        "payment_list": "💰 *Tasdiqlanmagan to'lovlar:*",
        "user_allowed": "✅ *Foydalanuvchi ruxsat berildi!*",
        "user_disallowed": "❌ *Foydalanuvchi ruxsat bekor qilindi!*",
        "set_admin_success": "👑 *Foydalanuvchi admin qilindi!*",
        "set_payment_amount": "💸 *Yangi to'lov summasini kiriting (masalan, 15.00):*",
        "payment_amount_updated": "✅ *To'lov summasi muvaffaqiyatli yangilandi!* 💰 *Yangi summa:* ${}",
        "invalid_payment_amount": "⚠️ *Noto'g'ri summa!* Iltimos, to'g'ri summa kiriting (masalan, 15.00)."
    },
    "ru": {
        "welcome": "🌟 *Добро пожаловать!* 🌟\nПожалуйста, выберите язык 👇",
        "questions_answers": "📝 Вопросы и ответы",
        "road_signs": "🚦 Дорожные знаки",
        "truck_parts": "🚚 Запчасти для грузовиков",
        "language_settings": "⚙️ Настройки языка",
        "success_message": "✅ *Поздравляем!* 🎉 Вы можете использовать бота! 🚀",
        "payment_required": "💰 Оплатите, чтобы использовать бота, и отправьте чек 📸",
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
        "next": "➡️ Следующая",
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
        # Admin xabarlar
        "admin_welcome": f"👑 *Добро пожаловать в админ-панель!* 🌟\n💰 *Текущая сумма платежа:* ${PAYMENT_AMOUNT}\nВыберите:",
        "add_question": "📝 *Процесс добавления вопроса начат!*",
        "add_road_sign": "🚦 *Процесс добавления дорожного знака начат!*",
        "add_truck_part": "🚚 *Процесс добавления запчасти начат!*",
        "delete_welcome": "🗑️ *Выберите язык для удаления:*",
        "delete_section": "📋 *Выберите раздел для удаления:*",
        "delete_item": "🔍 *Выберите элемент для удаления:*",
        "confirm_delete": "⚠️ *Подтвердите удаление?*",
        "payment_list": "💰 *Неподтвержденные платежи:*",
        "user_allowed": "✅ *Пользователю разрешено!*",
        "user_disallowed": "❌ *Разрешение у пользователя отозвано!*",
        "set_admin_success": "👑 *Пользователь назначен администратором!*",
        "set_payment_amount": "💸 *Введите новую сумму платежа (например, 15.00):*",
        "payment_amount_updated": "✅ *Сумма платежа успешно обновлена!* 💰 *Новая сумма:* ${}",
        "invalid_payment_amount": "⚠️ *Неверная сумма!* Пожалуйста, введите правильную сумму (например, 15.00)."
    },
    "es": {
        "welcome": "🌟 *¡Bienvenido!* 🌟\nPor favor, selecciona un idioma 👇",
        "questions_answers": "📝 Preguntas y respuestas",
        "road_signs": "🚦 Señales de tráfico",
        "truck_parts": "🚚 Piezas de camiones",
        "language_settings": "⚙️ Configuración de idioma",
        "success_message": "✅ *¡Felicidades!* 🎉 ¡Puedes usar el bot! 🚀",
        "payment_required": "💰 Paga para usar el bot y envía el recibo 📸",
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
        "next": "➡️ Siguiente",
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
        # Admin xabarlar
        "admin_welcome": f"👑 *¡Bienvenido al panel de administración!* 🌟\n💰 *Monto de pago actual:* ${PAYMENT_AMOUNT}\nElige:",
        "add_question": "📝 *¡Proceso de añadir pregunta iniciado!*",
        "add_road_sign": "🚦 *¡Proceso de añadir señal iniciado!*",
        "add_truck_part": "🚚 *¡Proceso de añadir pieza iniciado!*",
        "delete_welcome": "🗑️ *Elige un idioma para eliminar:*",
        "delete_section": "📋 *Elige una sección para eliminar:*",
        "delete_item": "🔍 *Elige un elemento para eliminar:*",
        "confirm_delete": "⚠️ *¿Confirmas la eliminación?*",
        "payment_list": "💰 *Pagos no confirmados:*",
        "user_allowed": "✅ *¡Permiso otorgado al usuario!*",
        "user_disallowed": "❌ *¡Permiso revocado al usuario!*",
        "set_admin_success": "👑 *¡Usuario designado como administrador!*",
        "set_payment_amount": "💸 *Ingresa el nuevo monto de pago (por ejemplo, 15.00):*",
        "payment_amount_updated": "✅ *¡Monto de pago actualizado con éxito!* 💰 *Nuevo monto:* ${}",
        "invalid_payment_amount": "⚠️ *¡Monto inválido!* Por favor, ingresa un monto correcto (por ejemplo, 15.00)."
    }
}


def get_message(language: str, key: str, *args) -> str:
    """Get localized message by language and key with fallback and formatting"""
    message = MESSAGES.get(language, MESSAGES["uz"]).get(key, MESSAGES["uz"].get(key, "Message not found"))
    return message.format(*args) if args else message


# Admin Menu
def get_admin_menu():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("📝 Savol Qo‘shish", callback_data="admin_add_question"),
        InlineKeyboardButton("🚦 Yo‘l Belgisi Qo‘shish", callback_data="admin_add_road_sign"),
        InlineKeyboardButton("🚚 Truck Zapchasti Qo‘shish", callback_data="admin_add_truck_part"),
        InlineKeyboardButton("🗑️ Ma‘lumot O‘chirish", callback_data="admin_delete"),
        InlineKeyboardButton("💰 To‘lovlarni Ko‘rish", callback_data="admin_payments"),
        InlineKeyboardButton("💸 To'lov Summasini O'zgartirish", callback_data="admin_set_payment_amount")
    )


# Language Selection
def get_language_selection():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🇺🇿 O‘zbek tili", callback_data="admin_lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский язык", callback_data="admin_lang_ru"),
        InlineKeyboardButton("🇪🇸 Español", callback_data="admin_lang_es")
    )


# Section Selection
def get_section_selection(language: str):
    sections = {
        "uz": ["Savol va Javoblar", "Yo'l Belgilari", "Truck Zapchastlari"],
        "ru": ["Вопросы и ответы", "Дорожные знаки", "Запчасти для грузовиков"],
        "es": ["Preguntas y respuestas", "Señales de tráfico", "Piezas de camiones"]
    }
    keyboard = InlineKeyboardMarkup(row_width=1)
    for text in sections.get(language, sections["uz"]):
        section = \
        {"Savol va Javoblar": "question", "Вопросы и ответы": "question", "Preguntas y respuestas": "question",
         "Yo'l Belgilari": "road_sign", "Дорожные знаки": "road_sign", "Señales de tráfico": "road_sign",
         "Truck Zapchastlari": "truck_part", "Запчасти для грузовиков": "truck_part",
         "Piezas de camiones": "truck_part"}[text]
        keyboard.add(InlineKeyboardButton(f"📌 {text}", callback_data=f"admin_section_{section}"))
    return keyboard


# Delete Items Keyboard
def get_delete_items_keyboard(items, section: str, language: str):
    keyboard = InlineKeyboardMarkup(row_width=1)
    item_types = {
        "uz": {"question": "Savol", "road_sign": "Yo'l belgisi", "truck_part": "Truck zapchasti"},
        "ru": {"question": "Вопрос", "road_sign": "Дорожный знак", "truck_part": "Запчасть грузовика"},
        "es": {"question": "Pregunta", "road_sign": "Señal de tráfico", "truck_part": "Pieza de camión"}
    }
    item_type = item_types.get(language, item_types["uz"]).get(section)
    for item in items:
        display_text = f"🔖 {item_type} #{item['id']}"
        if section == "question":
            display_text += f": {item['question'][:30]}{'...' if len(item['question']) > 30 else ''}"
        keyboard.add(InlineKeyboardButton(display_text, callback_data=f"delete_{section}_{item['id']}"))
    keyboard.add(InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin"))
    return keyboard


# Confirm Delete Button
def get_confirm_delete_button(section: str, item_id: int):
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"confirm_delete_{section}_{item_id}"),
        InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_delete")
    )


# Payment Actions Keyboard
def get_payment_actions(telegram_id: int):
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("✅ Ruxsat Berish", callback_data=f"allow_{telegram_id}"),
        InlineKeyboardButton("❌ Ruxsat Bekor Qilish", callback_data=f"disallow_{telegram_id}")
    )


# Config faylini yangilash funksiyasi
def update_payment_amount_in_config(new_amount: float):
    """data.config fayliga yangi to'lov summasini yozadi"""
    config_file = "data/config.py"
    try:
        # Faylni ochish va o'qish
        with open(config_file, "r") as file:
            lines = file.readlines()

        # PAYMENT_AMOUNT ni yangilash
        updated_lines = []
        amount_updated = False
        for line in lines:
            if line.strip().startswith("PAYMENT_AMOUNT ="):
                updated_lines.append(f"PAYMENT_AMOUNT = {new_amount}\n")
                amount_updated = True
            else:
                updated_lines.append(line)

        # Agar PAYMENT_AMOUNT topilmasa, qo'shish
        if not amount_updated:
            updated_lines.append(f"PAYMENT_AMOUNT = {new_amount}\n")

        # Faylni yangilash
        with open(config_file, "w") as file:
            file.writelines(updated_lines)
        logging.info(f"Config faylida PAYMENT_AMOUNT yangilandi: {new_amount}")
    except Exception as e:
        logging.error(f"Config faylini yangilashda xatolik: {e}")
        raise


# Admin Panel
@dp.message_handler(AdminFilter(), commands=["admin"])
async def admin_panel(message: types.Message):
    user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
    await message.answer(
        get_message(user_language, "admin_welcome"),
        reply_markup=get_admin_menu(),
        parse_mode="Markdown"
    )
    logging.info(f"Admin paneli ochildi: user_id={message.from_user.id}")


# Set Admin
@dp.message_handler(SuperAdminFilter(), commands=["setadmin"])
async def set_admin(message: types.Message):
    args = message.get_args()
    if not args:
        await message.answer("Foydalanuvchi ID sini kiriting: /setadmin <ID>")
        return
    try:
        telegram_id = int(args)
        user = await user_db.select_user(telegram_id=telegram_id)
        if not user:
            await message.answer(f"ID {telegram_id} topilmadi.")
            return
        await user_db.set_admin(telegram_id=telegram_id)
        user_language = user.get("language", "uz")
        await message.answer(
            get_message(user_language, "set_admin_success"),
            parse_mode="Markdown"
        )
        logging.info(f"Admin qilindi: telegram_id={telegram_id}")
    except ValueError:
        await message.answer("ID raqam bo'lishi kerak.")
    except Exception as e:
        logging.error(f"Admin o'rnatishda xatolik: {e}")
        await message.answer(get_message("uz", "error_occurred"), parse_mode="Markdown")


# Set Payment Amount
@dp.message_handler(SuperAdminFilter(), commands=["setpaymentamount"])
async def set_payment_amount_command(message: types.Message, state: FSMContext):
    args = message.get_args()
    user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
    if not args:
        await message.answer(
            get_message(user_language, "set_payment_amount"),
            parse_mode="Markdown"
        )
        await AdminStates.SET_PAYMENT_AMOUNT.set()
        return
    try:
        new_amount = float(args)
        if new_amount <= 0:
            raise ValueError("Summa noldan katta bo'lishi kerak")
        update_payment_amount_in_config(new_amount)
        global PAYMENT_AMOUNT
        PAYMENT_AMOUNT = new_amount
        await message.answer(
            get_message(user_language, "payment_amount_updated", new_amount),
            parse_mode="Markdown"
        )
        logging.info(f"To'lov summasi yangilandi: user_id={message.from_user.id}, new_amount={new_amount}")
    except ValueError:
        await message.answer(
            get_message(user_language, "invalid_payment_amount"),
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"To'lov summasini o'rnatishda xatolik: {e}")
        await message.answer(get_message("uz", "error_occurred"), parse_mode="Markdown")


# Handle Admin Actions
@dp.callback_query_handler(lambda c: c.data.startswith("admin_"))
async def handle_admin_action(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if not await user_db.check_if_admin(user_id):
        await callback_query.answer("Sizda admin huquqlari yo'q!", show_alert=True)
        return

    action = callback_query.data
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"
    await callback_query.message.delete()

    if action == "admin_payments":
        payments = await payment_db.get_pending_payments()
        if not payments:
            await callback_query.message.answer(
                get_message(user_language, "payment_list") + "\n🚫 *Hech qanday to'lov yo'q.*",
                parse_mode="Markdown"
            )
            return
        for payment in payments:
            user = await user_db.select_user(telegram_id=payment["telegram_id"])
            username = user.get("username", "Noma'lum") if user else "Noma'lum"
            safe_username = username.replace('@', '\@').replace('-', '\-').replace('.',
                                                                                   '\.') if username else "Noma'lum".replace(
                '@', '\@').replace('-', '\-').replace('.', '\.')
            created_at = payment.get("created_at", "").strftime('%Y-%m-%d %H:%M:%S') if hasattr(
                payment.get("created_at"), 'strftime') else str(payment.get("created_at", "Noma'lum")).replace('-',
                                                                                                               '\-')
            caption = (
                f"💰 *To'lov Cheki*\n\n"
                f"👤 ID: `{payment['telegram_id']}`\n"
                f"👤 Username: @{safe_username}\n"
                f"💰 Summa: ${payment['amount']}\n"
                f"📅 Vaqt: {created_at}\n"
            )
            try:
                await callback_query.message.answer_photo(
                    photo=payment["photo_file_id"],
                    caption=caption,
                    reply_markup=get_payment_actions(payment["telegram_id"]),
                    parse_mode="Markdown"
                )
            except Exception as e:
                logging.error(f"Failed to send payment photo to admin {user_id}: {e}, caption={caption}")
                await callback_query.message.answer_photo(
                    photo=payment["photo_file_id"],
                    caption=caption.replace('*', '').replace('`', ''),
                    reply_markup=get_payment_actions(payment["telegram_id"])
                )
        logging.info(f"To'lovlar ko'rildi: user_id={user_id}")
        return

    if action == "admin_delete":
        await callback_query.message.answer(
            get_message(user_language, "delete_welcome"),
            reply_markup=get_language_selection(),
            parse_mode="Markdown"
        )
        await AdminStates.DELETE_SELECT_LANGUAGE.set()
        logging.info(f"O'chirish boshlandi: user_id={user_id}")
        return

    if action == "admin_set_payment_amount":
        await callback_query.message.answer(
            get_message(user_language, "set_payment_amount"),
            parse_mode="Markdown"
        )
        await AdminStates.SET_PAYMENT_AMOUNT.set()
        logging.info(f"To'lov summasini o'zgartirish boshlandi: user_id={user_id}")
        return

    if action in ["admin_add_question", "admin_add_road_sign", "admin_add_truck_part"]:
        section = {"admin_add_question": "question", "admin_add_road_sign": "road_sign",
                   "admin_add_truck_part": "truck_part"}[action]
        await callback_query.message.answer(
            get_message(user_language, f"add_{section}"),
            reply_markup=get_language_selection(),
            parse_mode="Markdown"
        )
        await state.update_data(section=section)
        await AdminStates.SELECT_LANGUAGE.set()
        logging.info(f"Qo'shish boshlandi: user_id={user_id}, section={section}")
        return


# Set Payment Amount Handler
@dp.message_handler(state=AdminStates.SET_PAYMENT_AMOUNT)
async def handle_set_payment_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"
    try:
        new_amount = float(message.text)
        if new_amount <= 0:
            raise ValueError("Summa noldan katta bo'lishi kerak")
        update_payment_amount_in_config(new_amount)
        global PAYMENT_AMOUNT
        PAYMENT_AMOUNT = new_amount
        await message.answer(
            get_message(user_language, "payment_amount_updated", new_amount),
            reply_markup=get_admin_menu(),
            parse_mode="Markdown"
        )
        logging.info(f"To'lov summasi yangilandi: user_id={user_id}, new_amount={new_amount}")
    except ValueError:
        await message.answer(
            get_message(user_language, "invalid_payment_amount"),
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"To'lov summasini o'rnatishda xatolik: {e}")
        await message.answer(get_message(user_language, "error_occurred"), parse_mode="Markdown")
    finally:
        await state.finish()


# Language Selection (Add)
@dp.callback_query_handler(lambda c: c.data.startswith("admin_lang_"), state=AdminStates.SELECT_LANGUAGE)
async def handle_language_selection(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    lang = callback_query.data.split("_")[2]
    data = await state.get_data()
    section = data.get("section")
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"

    await state.update_data(language=lang)
    await callback_query.message.delete()

    if section == "question":
        await callback_query.message.answer(
            get_message(user_language, "add_question") + "\n📝 *Savol matnini kiriting:*",
            parse_mode="Markdown"
        )
        await AdminStates.ADD_QUESTION_TEXT.set()
    elif section == "road_sign":
        await callback_query.message.answer(
            get_message(user_language, "add_road_sign") + "\n🚦 *Rasmini yuboring:*",
            parse_mode="Markdown"
        )
        await AdminStates.ADD_ROAD_SIGN_IMAGE.set()
    elif section == "truck_part":
        await callback_query.message.answer(
            get_message(user_language, "add_truck_part") + "\n🚚 *Rasmini yuboring:*",
            parse_mode="Markdown"
        )
        await AdminStates.ADD_TRUCK_PART_IMAGE.set()
    logging.info(f"Til tanlandi: user_id={user_id}, section={section}, language={lang}")


# Question Text
@dp.message_handler(state=AdminStates.ADD_QUESTION_TEXT)
async def handle_question_text(message: types.Message, state: FSMContext):
    await state.update_data(question=message.text)
    user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
    await message.answer(
        get_message(user_language, "add_question") + "\n💡 *Javob matnini kiriting:*",
        parse_mode="Markdown"
    )
    await AdminStates.ADD_QUESTION_ANSWER.set()
    logging.info(f"Savol matni: user_id={message.from_user.id}, question={message.text}")


# Question Answer
@dp.message_handler(state=AdminStates.ADD_QUESTION_ANSWER)
async def handle_question_answer(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
    await message.answer(
        get_message(user_language, "add_question") + "\n🎵 *Audio faylni yuboring (o‘tkazib yuborish uchun /skip):*",
        parse_mode="Markdown"
    )
    await AdminStates.ADD_QUESTION_AUDIO.set()
    logging.info(f"Javob matni: user_id={message.from_user.id}, answer={message.text}")


# Skip Question Audio
@dp.message_handler(commands=["skip"], state=AdminStates.ADD_QUESTION_AUDIO)
async def skip_question_audio(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await sections_db.add_question(
            question=data["question"],
            answer=data["answer"],
            audio_file_id=None,
            language=data["language"]
        )
        user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
        await message.answer(
            get_message(user_language, "add_question") + "\n✅ *Savol muvaffaqiyatli qo‘shildi!*",
            parse_mode="Markdown"
        )
        logging.info(f"Savol qo'shildi: user_id={message.from_user.id}")
    except Exception as e:
        logging.error(f"Savol qo'shishda xatolik: {e}")
        await message.answer(get_message("uz", "error_occurred"), parse_mode="Markdown")
    finally:
        await state.finish()


# Handle Question Audio
@dp.message_handler(content_types=["audio"], state=AdminStates.ADD_QUESTION_AUDIO)
async def handle_question_audio(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await sections_db.add_question(
            question=data["question"],
            answer=data["answer"],
            audio_file_id=message.audio.file_id,
            language=data["language"]
        )
        user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
        await message.answer(
            get_message(user_language, "add_question") + "\n✅ *Savol va audio muvaffaqiyatli qo‘shildi!*",
            parse_mode="Markdown"
        )
        logging.info(f"Savol va audio qo'shildi: user_id={message.from_user.id}")
    except Exception as e:
        logging.error(f"Savol va audio qo'shishda xatolik: {e}")
        await message.answer(get_message("uz", "error_occurred"), parse_mode="Markdown")
    finally:
        await state.finish()


# Road Sign Image
@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=AdminStates.ADD_ROAD_SIGN_IMAGE)
async def handle_road_sign_image(message: types.Message, state: FSMContext):
    await state.update_data(image_file_id=message.photo[-1].file_id)
    user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
    await message.answer(
        get_message(user_language, "add_road_sign") + "\n📝 *Izoh matnini kiriting (o‘tkazib yuborish uchun /skip):*",
        parse_mode="Markdown"
    )
    await AdminStates.ADD_ROAD_SIGN_DESCRIPTION.set()
    logging.info(f"Yo'l belgisi rasmi: user_id={message.from_user.id}")


# Skip Road Sign Description
@dp.message_handler(commands=["skip"], state=AdminStates.ADD_ROAD_SIGN_DESCRIPTION)
async def skip_road_sign_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await sections_db.add_road_sign(
            image_file_id=data["image_file_id"],
            description=None,
            language=data["language"]
        )
        user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
        await message.answer(
            get_message(user_language, "add_road_sign") + "\n✅ *Yo'l belgisi muvaffaqiyatli qo‘shildi!*",
            parse_mode="Markdown"
        )
        logging.info(f"Yo'l belgisi qo'shildi: user_id={message.from_user.id}")
    except Exception as e:
        logging.error(f"Yo'l belgisi qo'shishda xatolik: {e}")
        await message.answer(get_message("uz", "error_occurred"), parse_mode="Markdown")
    finally:
        await state.finish()


# Road Sign Description
@dp.message_handler(state=AdminStates.ADD_ROAD_SIGN_DESCRIPTION)
async def handle_road_sign_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await sections_db.add_road_sign(
            image_file_id=data["image_file_id"],
            description=message.text,
            language=data["language"]
        )
        user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
        await message.answer(
            get_message(user_language, "add_road_sign") + "\n✅ *Yo'l belgisi muvaffaqiyatli qo‘shildi!*",
            parse_mode="Markdown"
        )
        logging.info(f"Yo'l belgisi qo'shildi: user_id={message.from_user.id}")
    except Exception as e:
        logging.error(f"Yo'l belgisi qo'shishda xatolik: {e}")
        await message.answer(get_message("uz", "error_occurred"), parse_mode="Markdown")
    finally:
        await state.finish()


# Truck Part Image
@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=AdminStates.ADD_TRUCK_PART_IMAGE)
async def handle_truck_part_image(message: types.Message, state: FSMContext):
    await state.update_data(image_file_id=message.photo[-1].file_id)
    user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
    await message.answer(
        get_message(user_language, "add_truck_part") + "\n📝 *Izoh matnini kiriting (o‘tkazib yuborish uchun /skip):*",
        parse_mode="Markdown"
    )
    await AdminStates.ADD_TRUCK_PART_DESCRIPTION.set()
    logging.info(f"Truck zapchasti rasmi: user_id={message.from_user.id}")


# Skip Truck Part Description
@dp.message_handler(commands=["skip"], state=AdminStates.ADD_TRUCK_PART_DESCRIPTION)
async def skip_truck_part_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await sections_db.add_truck_part(
            image_file_id=data["image_file_id"],
            description=None,
            language=data["language"]
        )
        user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
        await message.answer(
            get_message(user_language, "add_truck_part") + "\n✅ *Truck zapchasti muvaffaqiyatli qo‘shildi!*",
            parse_mode="Markdown"
        )
        logging.info(f"Truck zapchasti qo'shildi: user_id={message.from_user.id}")
    except Exception as e:
        logging.error(f"Truck zapchasti qo'shishda xatolik: {e}")
        await message.answer(get_message("uz", "error_occurred"), parse_mode="Markdown")
    finally:
        await state.finish()


# Truck Part Description
@dp.message_handler(state=AdminStates.ADD_TRUCK_PART_DESCRIPTION)
async def handle_truck_part_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await sections_db.add_truck_part(
            image_file_id=data["image_file_id"],
            description=message.text,
            language=data["language"]
        )
        user_language = await user_db.get_user_language(telegram_id=message.from_user.id) or "uz"
        await message.answer(
            get_message(user_language, "add_truck_part") + "\n✅ *Truck zapchasti muvaffaqiyatli qo‘shildi!*",
            parse_mode="Markdown"
        )
        logging.info(f"Truck zapchasti qo'shildi: user_id={message.from_user.id}")
    except Exception as e:
        logging.error(f"Truck zapchasti qo'shishda xatolik: {e}")
        await message.answer(get_message("uz", "error_occurred"), parse_mode="Markdown")
    finally:
        await state.finish()


# Delete Language Selection
@dp.callback_query_handler(lambda c: c.data.startswith("admin_lang_"), state=AdminStates.DELETE_SELECT_LANGUAGE)
async def delete_select_language(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    lang = callback_query.data.split("_")[2]
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"
    await state.update_data(language=lang)
    await callback_query.message.delete()
    await callback_query.message.answer(
        get_message(user_language, "delete_section"),
        reply_markup=get_section_selection(lang),
        parse_mode="Markdown"
    )
    await AdminStates.DELETE_SELECT_SECTION.set()
    logging.info(f"O'chirish til tanlandi: user_id={user_id}, language={lang}")


# Delete Section Selection
@dp.callback_query_handler(lambda c: c.data.startswith("admin_section_"), state=AdminStates.DELETE_SELECT_SECTION)
async def delete_select_section(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    section = callback_query.data.split("_")[2]
    data = await state.get_data()
    language = data.get("language")
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"

    try:
        items = (
            await sections_db.get_questions(language=language) if section == "question" else
            await sections_db.get_road_signs(language=language) if section == "road_sign" else
            await sections_db.get_truck_parts(language=language)
        )

        if not items:
            await callback_query.message.delete()
            await callback_query.message.answer(
                get_message(user_language, "no_data"),
                parse_mode="Markdown"
            )
            await state.finish()
            return

        await callback_query.message.delete()
        await callback_query.message.answer(
            get_message(user_language, "delete_item"),
            reply_markup=get_delete_items_keyboard(items, section, language),
            parse_mode="Markdown"
        )
        await state.update_data(section=section)
        await AdminStates.DELETE_SELECT_ITEM.set()
        logging.info(f"O'chirish bo'lim tanlandi: user_id={user_id}, section={section}")
    except Exception as e:
        logging.error(f"O'chirish bo'lim tanlashda xatolik: {e}")
        await callback_query.message.answer(get_message(user_language, "error_occurred"), parse_mode="Markdown")
        await state.finish()


# Delete Item Selection
@dp.callback_query_handler(lambda c: c.data.startswith("delete_"), state=AdminStates.DELETE_SELECT_ITEM)
async def delete_select_item(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    _, section, item_id = callback_query.data.split("_")
    item_id = int(item_id)
    data = await state.get_data()
    language = data.get("language")
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"

    try:
        item = (
            await sections_db.get_question_by_id(item_id) if section == "question" else
            await sections_db.get_road_sign_by_id(item_id) if section == "road_sign" else
            await sections_db.get_truck_part_by_id(item_id)
        )

        if not item:
            await callback_query.message.delete()
            await callback_query.answer(get_message(user_language, "item_not_found"), show_alert=True)
            await state.finish()
            return

        item_preview = item.get("question", item.get("description", ""))[:50] + "..." if len(
            item.get("question", item.get("description", ""))) > 50 else item.get("question",
                                                                                  item.get("description", ""))
        await callback_query.message.delete()
        await callback_query.message.answer(
            get_message(user_language,
                        "confirm_delete") + f"\n🔖 *{section.capitalize()} (ID: {item_id}): {item_preview}*",
            reply_markup=get_confirm_delete_button(section, item_id),
            parse_mode="Markdown"
        )
        await state.update_data(item_id=item_id)
        await AdminStates.DELETE_CONFIRM.set()
        logging.info(f"O'chirish element tanlandi: user_id={user_id}, section={section}, item_id={item_id}")
    except Exception as e:
        logging.error(f"O'chirish element tanlashda xatolik: {e}")
        await callback_query.message.answer(get_message(user_language, "error_occurred"), parse_mode="Markdown")
        await state.finish()


# Delete Confirmation
@dp.callback_query_handler(lambda c: c.data.startswith("confirm_delete_") or c.data == "cancel_delete",
                           state=AdminStates.DELETE_CONFIRM)
async def delete_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"

    if callback_query.data == "cancel_delete":
        await callback_query.message.delete()
        await callback_query.message.answer(
            get_message(user_language, "delete_welcome") + "\n🗑️ *O'chirish bekor qilindi.*",
            reply_markup=get_admin_menu(),
            parse_mode="Markdown"
        )
        await state.finish()
        logging.info(f"O'chirish bekor qilindi: user_id={user_id}")
        return

    try:
        _, _, section, item_id = callback_query.data.split("_")
        item_id = int(item_id)

        if section == "question":
            await sections_db.delete_question(item_id)
            success_msg = "✅ *Savol o'chirildi!*"
        elif section == "road_sign":
            await sections_db.delete_road_sign(item_id)
            success_msg = "✅ *Yo'l belgisi o'chirildi!*"
        else:
            await sections_db.delete_truck_part(item_id)
            success_msg = "✅ *Truck zapchasti o'chirildi!*"

        await callback_query.message.delete()
        await callback_query.message.answer(
            success_msg,
            reply_markup=get_admin_menu(),
            parse_mode="Markdown"
        )
        await state.finish()
        logging.info(f"Element o'chirildi: user_id={user_id}, section={section}, item_id={item_id}")
    except Exception as e:
        logging.error(f"Element o'chirishda xatolik: {e}")
        await callback_query.message.answer(get_message(user_language, "error_occurred"), parse_mode="Markdown")
        await state.finish()


# Handle Payment Actions
# admin.py, handle_payment_action funksiyasi
@dp.callback_query_handler(lambda c: c.data.startswith(("allow_", "disallow_")))
async def handle_payment_action(callback_query: types.CallbackQuery):
    """Handle payment actions"""
    user_id = callback_query.from_user.id
    action, telegram_id = callback_query.data.split("_")
    telegram_id = int(telegram_id)
    try:
        user_language = await user_db.get_user_language(telegram_id=user_id) or "uz"
        user = await user_db.select_user(telegram_id=telegram_id)
        payment = None
        for p in await payment_db.get_pending_payments():
            if p["telegram_id"] == telegram_id:
                payment = p
                break
        if not payment:
            await callback_query.answer("To'lov topilmadi yoki allaqachon ko'rib chiqilgan.", show_alert=True)
            return

        # Maxsus belgilarni ekranlash funksiyasi
        def escape_markdown_v2(text):
            """MarkdownV2 uchun maxsus belgilarni ekranlash"""
            special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            for char in special_chars:
                text = text.replace(char, f'\\{char}')
            return text

        # Ma'lumotlarni xavfsiz formatga o'tkazish
        username = user.get("username", "Noma'lum") or "Noma'lum"
        safe_username = escape_markdown_v2(username)

        # Vaqtni formatlash
        created_at = payment.get("created_at", "")
        if hasattr(created_at, 'strftime'):
            formatted_time = created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            formatted_time = str(created_at)
        safe_time = escape_markdown_v2(formatted_time)

        # Summani xavfsiz formatga o'tkazish
        safe_amount = escape_markdown_v2(str(payment['amount']))
        safe_telegram_id = escape_markdown_v2(str(telegram_id))

        if action == "allow":
            await user_db.update_user_permission(telegram_id=telegram_id, is_allowed=True)
            await payment_db.update_payment_status(payment_id=payment["id"], status="approved")
            await bot.send_message(
                telegram_id,
                get_message(user.get("language", "uz"), "user_allowed"),
                parse_mode="Markdown",
                protect_content=True
            )
            await callback_query.message.edit_caption(
                caption=(
                    f"💰 *To'lov Cheki*\n\n"
                    f"👤 ID: `{safe_telegram_id}`\n"
                    f"👤 Username: @{safe_username}\n"
                    f"💰 Summa: ${safe_amount}\n"
                    f"📅 Vaqt: {safe_time}\n"
                    f"✅ *Ruxsat berildi\\!*"
                ),
                parse_mode="MarkdownV2"
            )
            logging.info(f"✅ Ruxsat berildi: admin_id={user_id}, telegram_id={telegram_id}")
        elif action == "disallow":
            await user_db.update_user_permission(telegram_id=telegram_id, is_allowed=False)
            await payment_db.update_payment_status(payment_id=payment["id"], status="rejected")
            await bot.send_message(
                telegram_id,
                get_message(user.get("language", "uz"), "user_disallowed"),
                parse_mode="Markdown",
                protect_content=True
            )
            await callback_query.message.edit_caption(
                caption=(
                    f"💰 *To'lov Cheki*\n\n"
                    f"👤 ID: `{safe_telegram_id}`\n"
                    f"👤 Username: @{safe_username}\n"
                    f"💰 Summa: ${safe_amount}\n"
                    f"📅 Vaqt: {safe_time}\n"
                    f"❌ *Ruxsat bekor qilindi\\!*"
                ),
                parse_mode="MarkdownV2"
            )
            logging.info(f"❌ Ruxsat bekor qilindi: admin_id={user_id}, telegram_id={telegram_id}")
        await callback_query.answer()
    except Exception as e:
        logging.error(f"❌ To'lov harakatida xatolik: {e}")
        await callback_query.answer(get_message(user_language, "error_occurred"), show_alert=True)

@dp.message_handler(commands=['canceled'], state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    """Cancel command to reset state and return to appropriate menu"""
    user_id = message.from_user.id
    try:
        user = await user_db.select_user(telegram_id=user_id)
        user_language = user.get("language", "uz") if user else "uz"

        # Reset the current state
        await state.finish()

        # Update last active timestamp
        await user_db.update_last_active(telegram_id=user_id)

        # Check if the user is an admin
        is_admin = await user_db.check_if_admin(user_id) or str(user_id) in ADMINS

        if is_admin:
            # Return to admin menu for admins
            await message.answer(
                get_message(user_language, "admin_welcome"),
                reply_markup=get_admin_menu(),
                parse_mode="Markdown",
                protect_content=True
            )
            logging.info(f"Cancel command executed (admin): user_id={user_id}, language={user_language}")
        else:
            # Return to main user menu for non-admins
            await message.answer(
                get_message(user_language, "select_section"),
                reply_markup=await get_admin_menu(user_language),
                parse_mode="Markdown",
                protect_content=True
            )
            logging.info(f"Cancel command executed (user): user_id={user_id}, language={user_language}")

    except Exception as e:
        logging.error(f"Error in cancel command: user_id={user_id}, error={e}")
        await message.answer(
            get_message("uz", "error_occurred"),
            parse_mode="Markdown",
            protect_content=True
        )