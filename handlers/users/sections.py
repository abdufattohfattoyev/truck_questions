# from aiogram import types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from loader import dp, bot, user_db, sections_db
# import logging
#
# def get_section_items_keyboard(items, section: str, language: str):
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     messages = {
#         "uz": {"question": "Savol", "road_sign": "Yo'l belgisi", "truck_part": "Truck zapchasti"},
#         "ru": {"question": "Вопрос", "road_sign": "Дорожный знак", "truck_part": "Запчасть грузовика"},
#         "es": {"question": "Pregunta", "road_sign": "Señal de tráfico", "truck_part": "Pieza de camión"}
#     }
#     for item in items:
#         item_type = messages[language][section] if language in messages else messages["uz"][section]
#         keyboard.add(InlineKeyboardButton(f"{item_type} {item['id']}", callback_data=f"{section}_{item['id']}"))
#     return keyboard
#
# @dp.message_handler(lambda message: message.text in [
#     "Savol va Javoblar", "Yo'l Belgilari", "Truck Zapchastlari",
#     "Вопросы и ответы", "Дорожные знаки", "Запчасти для грузовиков",
#     "Preguntas y respuestas", "Señales de tráfico", "Piezas de camiones"
# ])
# async def handle_section_selection(message: types.Message):
#     user_id = message.from_user.id
#     user_language = user_db.get_user_language(telegram_id=user_id)
#     logging.info(f"Bo'lim tanlandi: user_id={user_id}, text={message.text}")
#
#     if not user_db.check_if_allowed(telegram_id=user_id):
#         messages = {
#             "uz": "❌ Botdan foydalanishga ruxsat yo'q. To'lov qiling.",
#             "ru": "❌ Нет доступа к боту. Оплатите.",
#             "es": "❌ No tienes acceso al bot. Realiza el pago."
#         }
#         await message.answer(messages.get(user_language, "❌ Ruxsat yo'q."), protect_content=True)
#         return
#
#     user_db.update_last_active(telegram_id=user_id)
#     section_map = {
#         "Savol va Javoblar": "question", "Вопросы и ответы": "question", "Preguntas y respuestas": "question",
#         "Yo'l Belgilari": "road_sign", "Дорожные знаки": "road_sign", "Señales de tráfico": "road_sign",
#         "Truck Zapchastlari": "truck_part", "Запчасти для грузовиков": "truck_part", "Piezas de camiones": "truck_part"
#     }
#     section = section_map.get(message.text)
#     if section == "question":
#         items = sections_db.get_questions(language=user_language)
#     elif section == "road_sign":
#         items = sections_db.get_road_signs(language=user_language)
#     else:
#         items = sections_db.get_truck_parts(language=user_language)
#
#     if not items:
#         messages = {
#             "uz": "Bu bo'limda ma'lumot yo'q.",
#             "ru": "В этом разделе нет данных.",
#             "es": "No hay datos en esta sección."
#         }
#         await message.answer(messages.get(user_language, "Ma'lumot yo'q."), protect_content=True)
#         return
#
#     await message.answer(f"{message.text} ro'yxati:", reply_markup=get_section_items_keyboard(items, section, user_language))
#     logging.info(f"Bo'lim ro'yxati yuborildi: user_id={user_id}, section={section}")
#
# @dp.callback_query_handler(lambda c: c.data.startswith(("question_", "road_sign_", "truck_part_")))
# async def handle_item_selection(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     user_language = user_db.get_user_language(telegram_id=user_id)
#     section, item_id = callback_query.data.split("_", 1)
#     item_id = int(item_id)
#     logging.info(f"Element tanlandi: user_id={user_id}, section={section}, item_id={item_id}")
#
#     if not user_db.check_if_allowed(telegram_id=user_id):
#         messages = {
#             "uz": "❌ Botdan foydalanishga ruxsat yo'q. To'lov qiling.",
#             "ru": "❌ Нет доступа к боту. Оплатите.",
#             "es": "❌ No tienes acceso al bot. Realiza el pago."
#         }
#         await callback_query.message.delete()
#         await callback_query.answer(messages.get(user_language, "❌ Ruxsat yo'q."), show_alert=True)
#         return
#
#     if section == "question":
#         item = sections_db.get_questions(language=user_language)
#         item = next((i for i in item if i["id"] == item_id), None)
#         if item:
#             await callback_query.message.delete()
#             await bot.send_message(user_id, f"Savol: {item['question']}\nJavob: {item['answer']}", protect_content=True)
#             if item["audio_file_id"]:
#                 await bot.send_audio(user_id, item["audio_file_id"], protect_content=True)
#             logging.info(f"Savol yuborildi: user_id={user_id}, item_id={item_id}")
#     elif section == "road_sign":
#         item = sections_db.get_road_signs(language=user_language)
#         item = next((i for i in item if i["id"] == item_id), None)
#         if item:
#             await callback_query.message.delete()
#             caption = item["description"] or ""
#             await bot.send_photo(user_id, item["image_file_id"], caption=caption, protect_content=True)
#             logging.info(f"Yo'l belgisi yuborildi: user_id={user_id}, item_id={item_id}")
#     elif section == "truck_part":
#         item = sections_db.get_truck_parts(language=user_language)
#         item = next((i for i in item if i["id"] == item_id), None)
#         if item:
#             await callback_query.message.delete()
#             caption = item["description"] or ""
#             await bot.send_photo(user_id, item["image_file_id"], caption=caption, protect_content=True)
#             logging.info(f"Truck zapchasti yuborildi: user_id={user_id}, item_id={item_id}")