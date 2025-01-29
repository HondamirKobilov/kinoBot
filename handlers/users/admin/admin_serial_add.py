import random
from data.config import private_channel, asosiy_channel, asosiy_bot
from handlers.users.admin.kino_kod import CodeManager
from keyboards.inline.inline_admin import create_serials_keyboard, admin_back_menu, create_serial_parts_keyboard, \
    create_confirmation_keyboard, create_part_action_keyboard, create_confirmation_keyboard_part, \
    create_part_action_buttons
from keyboards.inline.inline_user import move_download
from loader import dp, bot
from aiogram import types
from filters import F
from states.admin import SerialCreation, QismCreation
from utils.database.functions.f_serial import fetch_all_serials, create_serial, fetch_serial_parts, fetch_serial_by_id, \
    check_qism_exists, get_serial_name_by_id, create_qism, \
    delete_serial_and_parts, fetch_parts_by_serial_id, get_serial_by_id, update_serial_name, delete_part_by_id, \
    get_part_by_id, update_part_name_in_db, update_part_info_in_db, delete_part_by_id1
from aiogram.dispatcher import FSMContext
code_manager = CodeManager()
def generate_serial_kod():
    return code_manager.generate_kod()
def format_size(size_bytes):
    size_mb = size_bytes / (1024 * 1024)
    if size_mb < 1000:
        return f"{size_mb:.2f} MB"
    else:
        size_gb = size_mb / 1024
        return f"{size_gb:.2f} GB"

@dp.callback_query_handler(F.AdminFilter(), text="admin_seriallar", state="*")
async def handle_admin_serials(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    serials = await fetch_all_serials()
    keyboard = await create_serials_keyboard(serials, page=0)
    if serials:
        await callback_query.message.edit_text("📺 Bazadagi seriallar:", reply_markup=keyboard)
    else:
        await callback_query.message.edit_text("❗️ Hozircha hech qanday serial mavjud emas.", reply_markup=keyboard)

@dp.callback_query_handler(F.AdminFilter(), text_startswith="admin_slide_serial_", state="*")
async def handle_slide_serials(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")
    page = int(data[-1])  # Joriy sahifa raqami
    serials = await fetch_all_serials()
    keyboard = await create_serials_keyboard(serials, page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(F.AdminFilter(), text="add_serial", state="*")
async def prompt_serial_name(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Iltimos, Serial nomini kiriting:", reply_markup=admin_back_menu)
    await SerialCreation.waiting_for_serial_name.set()
    await callback_query.answer()

@dp.message_handler(F.AdminFilter(), state=SerialCreation.waiting_for_serial_name)
async def add_serial(message: types.Message, state: FSMContext):
    serial_name = message.text.strip()
    new_serial = await create_serial(serial_nomi=serial_name)
    if new_serial:
        serials = await fetch_all_serials()
        keyboard = await create_serials_keyboard(serials)
        await message.answer(f"Serial '{serial_name}' muvaffaqiyatli qo'shildi 🎉", reply_markup=keyboard)
    else:
        await message.answer("Serialni qo'shishda muammo yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    await state.finish()

@dp.callback_query_handler(F.AdminFilter(), text_startswith="serial_", state="*")
async def show_serial_parts(callback_query: types.CallbackQuery, state: FSMContext):
    serial_id = int(callback_query.data.split("_")[1])
    serial = await fetch_serial_by_id(serial_id)
    parts = await fetch_serial_parts(serial_id)
    keyboard = await create_serial_parts_keyboard(serial_id, page=0)
    if parts:
        await callback_query.message.edit_text(
            text=f"<b>🎞 {serial.serial_nomi}</b> serialining qismlari:",
            reply_markup=keyboard
        )
    else:
        await callback_query.message.edit_text(
            f"<b>❗️{serial.serial_nomi}</b> serialga hali qismlar qo'shilmagan.",
            reply_markup=keyboard
        )
@dp.callback_query_handler(F.AdminFilter(), text_startswith="slide_parts_", state="*")
async def slide_serial_parts(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")
    serial_id = int(data[2])
    page = int(data[3])  # Joriy sahifa raqami
    keyboard = await create_serial_parts_keyboard(serial_id, page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()
@dp.callback_query_handler(F.AdminFilter(), text_startswith="add_part_", state="*"   )
async def start_add_part(callback_query: types.CallbackQuery, state: FSMContext):
    serial_id = int(callback_query.data.split("_")[2])
    await QismCreation.waiting_for_tizer.set()
    await callback_query.message.edit_text("Iltimos, serial qismi uchun tizer yuklang (video yoki rasm):", reply_markup=admin_back_menu)
    await state.update_data(serial_id=serial_id)

@dp.message_handler(F.AdminFilter(), content_types=['video', 'photo'], state=QismCreation.waiting_for_tizer)
async def kino_tizer(message: types.Message, state: FSMContext):
    if message.content_type == 'video':
        tizer_file_id = message.video.file_id
    elif message.content_type == 'photo':
        tizer_file_id = message.photo[-1].file_id
    await state.update_data(tizerFile_id=tizer_file_id, tizer_type=message.content_type)
    await QismCreation.next()
    await message.answer("Endi kino nomini kiriting:", reply_markup=admin_back_menu)


@dp.message_handler(F.AdminFilter(), state=QismCreation.waiting_for_kino_nomi)
async def kino_nomi(message: types.Message, state: FSMContext):
    kino_nomi = message.text
    data = await state.get_data()
    serial_id = data.get("serial_id")
    exists = await check_qism_exists(serial_id, kino_nomi)
    if exists:
        await message.answer(
            f"Bu serial uchun '{kino_nomi}' nomli qism allaqachon mavjud. Iltimos, boshqa nom kiriting:",
            reply_markup=admin_back_menu
        )
        return
    await state.update_data(kino_nomi=kino_nomi)
    await QismCreation.next()
    await message.answer("Endi kino haqida ma'lumot kiriting:", reply_markup=admin_back_menu)

@dp.message_handler(F.AdminFilter(), state=QismCreation.waiting_for_kino_info)
async def kino_info(message: types.Message, state: FSMContext):
    await state.update_data(kino_info=message.text)
    await QismCreation.next()
    await message.answer("Endi kinoni yuklang:", reply_markup=admin_back_menu)

@dp.message_handler(F.AdminFilter(), content_types=['video'], state=QismCreation.waiting_for_kino)
async def kino_file(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    channel_id = private_channel
    tizer_file_id = user_data['tizerFile_id']
    sent_message = await message.bot.send_video(chat_id=channel_id, video=message.video.file_id)
    kino_size = format_size(sent_message.video.file_size)
    kod = generate_serial_kod()
    serial_id = user_data.get("serial_id")
    serial_nomi = await get_serial_name_by_id(serial_id)
    caption_tizer = (f"<b>Ushbu serialni botimizga joyladik</b>\n\n"
                     f"ℹ️ {user_data['kino_info']}\n\n"
                     f"<i>Filmni yuklab olish uchun botimizga kiring va kodni kiriting</i>\n\n"
                     f"🔑 Kod: <b><i>{kod}</i></b>\n\n"
                     f"👉{asosiy_channel}")
    caption_tizer1 = (f"🎞 Serial nomi: <b>{serial_nomi}</b>\n"
                      f"🔸 Yangi qism: <b>{user_data['kino_nomi']}</b>\n"
                     f"ℹ️ Kino haqida: {user_data['kino_info']}\n"
                      f"💾 Hajmi: {kino_size}\n"
                     f"🔑 Kod: {kod}\n"
                     f"🔗 Bot: <a href='{asosiy_bot}?start=havola_click_{kod}'>Havola</a>\n\n"
                     f"👉{asosiy_channel}")
    type = user_data['tizer_type']
    if type == 'video':
        asosiy_tizer_message_id = await message.bot.send_video(chat_id=asosiy_channel, video=tizer_file_id, caption=caption_tizer, reply_markup=move_download(kod))
        tizer_message = await message.bot.send_video(chat_id=channel_id, video=tizer_file_id, caption=caption_tizer1)
    else:
        asosiy_tizer_message_id =  await message.bot.send_photo(chat_id=asosiy_channel, photo=tizer_file_id, caption=caption_tizer, reply_markup=move_download(kod))
        tizer_message = await message.bot.send_photo(chat_id=channel_id, photo=tizer_file_id, caption=caption_tizer1)
    message_id = sent_message.message_id
    await state.update_data(kinoMessage_id=message_id, kino_hajmi=kino_size)
    await create_qism(
        kod=kod,
        tizer_message_id=tizer_message.message_id,
        asosiy_tizer_message_id=asosiy_tizer_message_id.message_id,
        kino_message_id=message_id,
        serial_nomi=user_data['kino_nomi'],
        serial_info=user_data['kino_info'],
        serial_hajmi=kino_size,
        serial_id=serial_id
    )
    await message.answer(f"Yangi qism muvaffaqiyatli qo'shildi: <b>{user_data['kino_nomi']} ({kino_size})</b> 🎉",
                         reply_markup=await create_serial_parts_keyboard(serial_id=serial_id, page=0))

@dp.callback_query_handler(F.AdminFilter(), lambda call: call.data.startswith("delete_serial_"), state="*")
async def ask_delete_confirmation(callback_query: types.CallbackQuery):
    serial_id = int(callback_query.data.split("_")[2])
    serial_nomi = await get_serial_name_by_id(serial_id)
    keyboard = create_confirmation_keyboard(serial_id)
    await callback_query.message.edit_text(
        f"<b>{serial_nomi}</b> serialni va unga tegishli qismlarni o'chirishni xohlaysizmi?",
        reply_markup=keyboard
    )

@dp.callback_query_handler(F.AdminFilter(), lambda call: call.data.startswith("confirmserial_delete_"), state="*")
async def delete_serial(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        serial_id = int(callback_query.data.split("_")[2])
        serial_nomi = await get_serial_name_by_id(serial_id)
        parts = await fetch_parts_by_serial_id(serial_id)
        for part in parts:
            try:
                if part.tizer_message_id:
                    await bot.delete_message(chat_id=private_channel, message_id=part.tizer_message_id)
                if part.kino_message_id:
                    await bot.delete_message(chat_id=private_channel, message_id=part.kino_message_id)
                if part.asosiy_tizer_message_id:
                    await bot.delete_message(chat_id=asosiy_channel, message_id=part.asosiy_tizer_message_id)
            except Exception as e:
                print(f"Xatolik: {part.id} qismining xabarini o'chirishda muammo: {e}")
        success = await delete_serial_and_parts(serial_id)
        serials = await fetch_all_serials()
        keyboard = await create_serials_keyboard(serials)

        if success:
            await callback_query.message.edit_text(
                f"<b>{serial_nomi}</b> serial va unga tegishli qismlar muvaffaqiyatli o'chirildi 🎉",
                reply_markup=keyboard
            )
        else:
            await callback_query.message.answer(
                f"Xatolik yuz berdi: Serial ID {serial_id} o'chirilmadi."
            )
    except Exception as e:
        await callback_query.message.answer(f"Xatolik yuz berdi: {str(e)}")

@dp.callback_query_handler(F.AdminFilter(), lambda call: call.data == "cancelserial_delete", state="*")
async def cancel_delete(callback_query: types.CallbackQuery):
    try:
        serials = await fetch_all_serials()
        keyboard = await create_serials_keyboard(serials)
        await callback_query.message.edit_text(
            "Serialni o'chirish bekor qilindi.",
            reply_markup=keyboard
        )
    except Exception as e:
        await callback_query.message.answer(f"Xatolik yuz berdi: {str(e)}")
@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('edit_serialname_'), state="*")
async def ask_edit_serial_name(callback_query: types.CallbackQuery, state: FSMContext):
    serial_id = int(callback_query.data.split("_")[2])
    serial = await get_serial_by_id(serial_id)  # Serialni bazadan olish
    if not serial:
        await callback_query.message.answer("Serial topilmadi.")
        return
    await state.update_data(serial_id=serial_id)
    await state.set_state("waiting_for_new_serial_name")
    await callback_query.message.edit_text(
        f"Hozirgi serial nomi: <b>{serial.serial_nomi}</b>\nYangi nomni kiriting:",
        parse_mode="HTML"
    )
@dp.message_handler(F.AdminFilter(), state="waiting_for_new_serial_name", content_types=types.ContentType.TEXT)
async def edit_serial_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    serial_id = data["serial_id"]
    public_message_id = data.get("public_message_id")
    keyboard = await create_serial_parts_keyboard(serial_id, page=0)
    new_serial_name = message.text.strip()
    try:
        await update_serial_name(serial_id, new_serial_name)
        await message.answer(f"Serial nomi muvaffaqiyatli yangilandi🎉: <b>{new_serial_name}</b>", parse_mode="HTML", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")
    finally:
        await state.finish()
@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('part_'), state="*")
async def show_part_details(callback_query: types.CallbackQuery):
    part_id = int(callback_query.data.split("_")[1])
    part = await get_part_by_id(part_id)
    if not part:
        await callback_query.message.answer("Qism topilmadi.")
        return
    text = (
        f"🎞 <b>Kino nomi:</b> {part.serial_nomi}\n"
        f"💾 <b>Hajmi:</b> {part.serial_hajmi}\n"
        f"ℹ️ <b>Info:</b> {part.serial_info}"
    )
    keyboard = create_part_action_keyboard(part_id)
    await callback_query.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('edit_part_name_'), state="*")
async def edit_part_name(callback_query: types.CallbackQuery, state: FSMContext):
    part_id = int(callback_query.data.split("_")[3])
    part = await get_part_by_id(part_id)
    if not part:
        await callback_query.message.answer("Qism topilmadi.")
        return
    await state.update_data(part_id=part_id)
    await state.set_state("waiting_for_new_part_name")
    await callback_query.message.edit_text(
        f"Hozirgi nomi: <b>{part.serial_nomi}</b>\nYangi nomni kiriting:",
        parse_mode="HTML"
    )
@dp.message_handler(F.AdminFilter(), state="waiting_for_new_part_name", content_types=types.ContentType.TEXT)
async def update_part_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    part_id = data["part_id"]
    new_name = message.text.strip()
    try:
        updated = await update_part_name_in_db(part_id, new_name)
        if updated:
            part = await get_part_by_id(part_id)
            if not part:
                await message.answer("❌ Qism topilmadi.")
                await state.finish()
                return
            serial_id = part.serial_id
            kino_info = part.serial_info
            kino_hajmi = part.serial_hajmi
            tizer_message_id = part.tizer_message_id
            kod = part.kod
            serial_name = await get_serial_name_by_id(serial_id=serial_id)
            caption_tizer1 = (
                f"🎞 Serial nomi: <b>{serial_name}</b>\n"
                f"🔸 Yangi qism: <b>{new_name}</b>\n"
                f"ℹ️ Kino haqida: {kino_info}\n"
                f"💾 Hajmi: {kino_hajmi}\n"
                f"🔑 Kod: {kod}\n"
                f"🔗 Bot: <a href='{asosiy_bot}?start=havola_click_{kod}'>Havola</a>\n\n"
                f"👉{asosiy_channel}"
            )
            try:
                await bot.edit_message_caption(
                    chat_id=private_channel,  # Tegishli kanal ID
                    message_id=tizer_message_id,  # Tizer post ID
                    caption=caption_tizer1,
                    parse_mode="HTML"
                )
                await message.answer("Telegram kanaldagi post muvaffaqiyatli yangilandi!")
            except Exception as e:
                await message.answer(f"❌ Telegram kanaldagi postni tahrirlashda xatolik yuz berdi: {str(e)}")
            text = (
                f"🎞 <b>Kino nomi:</b> {new_name}\n"
                f"💾 <b>Hajmi:</b> {kino_hajmi}\n"
                f"ℹ️ <b>Info:</b> {kino_info}"
            )
            keyboard = create_part_action_buttons(part_id, part.serial_id)
            await message.answer(f"Qism nomi yangilandi 🎉\n\n{text}", parse_mode="HTML", reply_markup=keyboard)
        else:
            await message.answer("❌ Qism nomini yangilashda xatolik yuz berdi.")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
    finally:
        await state.finish()

@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('edit_part_info_'), state="*")
async def edit_part_info(callback_query: types.CallbackQuery, state: FSMContext):
    part_id = int(callback_query.data.split("_")[3])
    part = await get_part_by_id(part_id)

    if not part:
        await callback_query.message.answer("❌ Qism topilmadi.")
        return
    await state.update_data(part_id=part_id)
    await state.set_state("waiting_for_new_part_info")
    await callback_query.message.edit_text(
        f"Hozirgi ma'lumot:\n<b>{part.serial_info}</b>\n\nYangi ma'lumotni kiriting:",
        parse_mode="HTML"
    )

@dp.message_handler(F.AdminFilter(), state="waiting_for_new_part_info", content_types=types.ContentType.TEXT)
async def update_part_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    part_id = data["part_id"]
    new_info = message.text.strip()
    try:
        updated = await update_part_info_in_db(part_id, new_info)
        if updated:
            part = await get_part_by_id(part_id)
            if not part:
                await message.answer("❌ Qism topilmadi.")
                await state.finish()
                return

            serial_id = part.serial_id
            serial_name = await get_serial_name_by_id(serial_id)
            tizer_message_id = part.tizer_message_id
            asosiy_tizer_message_id = part.asosiy_tizer_message_id
            kod = part.kod
            kino_hajmi = part.serial_hajmi

            # Yangilangan caption
            caption_tizer = (
                f"<b>Ushbu serialni botimizga joyladik</b>\n\n"
                f"ℹ️ {new_info}\n\n"
                f"<i>Filmni yuklab olish uchun botimizga kiring va kodni kiriting</i>\n\n"
                f"🔑 Kod: <b><i>{kod}</i></b>\n\n"
                f"👉{asosiy_channel}"
            )
            caption_tizer1 = (
                f"🎞 Serial nomi: <b>{serial_name}</b>\n"
                f"🔸 Qism ma'lumotlari: <b>{new_info}</b>\n"
                f"💾 Hajmi: {kino_hajmi}\n"
                f"🔑 Kod: {kod}\n"
                f"🔗 Bot: <a href='{asosiy_bot}?start=havola_click_{kod}'>Havola</a>\n\n"
                f"👉{asosiy_channel}"
            )
            try:
                await bot.edit_message_caption(
                    chat_id=private_channel,  # Private kanal ID
                    message_id=tizer_message_id,
                    caption=caption_tizer1,
                    parse_mode="HTML"
                )
                await bot.edit_message_caption(
                    chat_id=asosiy_channel,  # Asosiy kanal ID
                    message_id=asosiy_tizer_message_id,
                    caption=caption_tizer,
                    reply_markup=move_download(kod),
                    parse_mode="HTML"
                )
                await message.answer("Telegram kanaldagi post muvaffaqiyatli yangilandi!")
            except Exception as e:
                await message.answer(f"❌ Telegram kanaldagi postni tahrirlashda xatolik yuz berdi: {str(e)}")

            # Yangilangan ma'lumotni foydalanuvchiga ko'rsatish
            text = (
                f"🎞 <b>Serial nomi:</b> {serial_name}\n"
                f"💾 <b>Hajmi:</b> {kino_hajmi}\n"
                f"ℹ️ <b>Info:</b> {new_info}"
            )
            keyboard = create_part_action_buttons(part_id, serial_id)
            await message.answer(f"Qism ma'lumoti yangilandi 🎉\n\n{text}", parse_mode="HTML", reply_markup=keyboard)
        else:
            await message.answer("❌ Qism ma'lumotini yangilashda xatolik yuz berdi.")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
    finally:
        await state.finish()


@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('delete_part_'), state="*")
async def confirm_delete_part(callback_query: types.CallbackQuery):
    try:
        part_id = int(callback_query.data.split("_")[2])
        part = await get_part_by_id(part_id)

        if not part:
            await callback_query.message.answer("Qism topilmadi yoki o'chirilgan.")
            return

        keyboard = create_confirmation_keyboard_part(part_id)  # Tasdiqlash tugmalarini yaratish

        await callback_query.message.edit_text(
            f"Rostdan <b>{part.serial_nomi}</b> qismi o'chirilsinmi?",
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        await callback_query.message.answer(f"Xatolik yuz berdi: {str(e)}")


@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith("partt_cancel_delete_"), state="*")
async def cancel_delete_part(callback_query: types.CallbackQuery):
    try:
        serial_id = int(callback_query.data.split("_")[-1])
        parts = await fetch_serial_parts(serial_id)
        keyboard = await create_serial_parts_keyboard(serial_id, page=0)

        await callback_query.message.edit_text(
            "O'chirish bekor qilindi! ❌",
            reply_markup=keyboard
        )
    except Exception as e:
        await callback_query.message.answer(f"Xatolik yuz berdi: {str(e)}")


@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('partt_confirm_delete_'), state="*")
async def delete_part(callback_query: types.CallbackQuery):
    try:
        part_id = int(callback_query.data.split("_")[-1])
        part = await get_part_by_id(part_id)

        if not part:
            await callback_query.message.answer("Qism topilmadi yoki o'chirilgan.")
            return
        deleted = await delete_part_by_id(part_id)
        if deleted:
            parts = await fetch_serial_parts(part.serial_id)
            keyboard = await create_serial_parts_keyboard(part.serial_id, page=0)
            await callback_query.message.edit_text(
                f"<b>{part.serial_nomi}</b> muvaffaqiyatli o'chirildi! 🎉",
                parse_mode="HTML",
                reply_markup=keyboard
            )
        else:
            await callback_query.message.answer("Qism o'chirishda xatolik yuz berdi.")
    except Exception as e:
        await callback_query.message.answer(f"Xatolik yuz berdi: {str(e)}")
# @dp.callback_query_handler(lambda c: c.data.startswith('part_'), state="*")
# async def show_serial_part_details(callback_query: types.CallbackQuery):
#     part_id = int(callback_query.data.split("_")[1])
#     part = await get_part_by_id(part_id)
#     if not part:
#         await callback_query.answer("❌ Qism topilmadi.")
#         return
#     text = (
#         f"🎬 <b>Nomi:</b> {part.serial_info}\n\n"
#         f"📄 <b>Kino haqida:</b> {part.serial_hajmi}\n\n"
#         f"💾 <b>Hajmi:</b> {part.kino_message_id or 'Maʼlumot yoʻq'}"
#     )
#     keyboard = create_part_action_buttons(part_id=part.kod, serial_id=part.serial_id)
#
#     await callback_query.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)

