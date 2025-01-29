from data.config import private_channel, asosiy_bot, asosiy_channel
from handlers.users.admin.kino_kod import CodeManager
from keyboards.inline.inline_admin import create_kino_keyboard, admin_back_menu, kino_details_keyboard, \
    create_kino_confirmation_keyboard
from keyboards.inline.inline_user import move_download
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.admin import KinoCreation, KinoCreation_Edit
from utils.database.functions.f_kino import get_all_kinolar, create_kino, check_kino_exists, get_kino_by_kod, \
    update_kino, delete_kino_by_kod
from filters import F
from utils.database.functions.f_serial import update_serial_name, get_serial_by_id

code_manager = CodeManager()
def generate_kino_kod():
    return code_manager.generate_kod()
def format_size(size_bytes):
    size_mb = size_bytes / (1024 * 1024)
    if size_mb < 1000:
        return f"{size_mb:.2f} MB"
    else:
        size_gb = size_mb / 1024
        return f"{size_gb:.2f} GB"
@dp.callback_query_handler(F.AdminFilter(), text="admin_kinolar", state="*")
async def show_kinolar(callback_query: types.CallbackQuery):
    kinolar = await get_all_kinolar()
    keyboard = create_kino_keyboard(kinolar)
    if not kinolar:
        await callback_query.message.edit_text("❗️ Sizda hali kino mavjud emas.", reply_markup=keyboard)
    else:
        await callback_query.message.edit_text("🎬 Mavjud kinolar:", reply_markup=keyboard)

@dp.callback_query_handler(F.AdminFilter(), text="add_kino")
async def add_kino_start(callback_query: types.CallbackQuery):
    await KinoCreation.waiting_for_tizer.set()
    await callback_query.message.edit_text("Kino qo'shish uchun iltimos kino tizerini yuklang:", reply_markup=admin_back_menu)

@dp.message_handler(F.AdminFilter(), content_types=['video', 'photo'], state=KinoCreation.waiting_for_tizer)
async def kino_tizer(message: types.Message, state: FSMContext):
    # Fayl identifikatorini saqlash, kanalga yuborish emas
    if message.content_type == 'video':
        tizer_file_id = message.video.file_id
    elif message.content_type == 'photo':
        tizer_file_id = message.photo[-1].file_id
    await state.update_data(tizerFile_id=tizer_file_id, tizer_type=message.content_type)
    await KinoCreation.next()
    await message.answer("Endi kino nomini kiriting:", reply_markup=admin_back_menu)


@dp.message_handler(F.AdminFilter(), state=KinoCreation.waiting_for_kino_nomi)
async def kino_nomi(message: types.Message, state: FSMContext):
    kino_nomi = message.text
    exists = await check_kino_exists(kino_nomi)  # Kino nomini tekshirish
    if exists:
        await message.answer("Bunday nomli kino oldin yuklangan. Iltimos boshqa kino nomi kiriting:", reply_markup=admin_back_menu)
        return
    await state.update_data(kino_nomi=kino_nomi)
    await KinoCreation.next()
    await message.answer("Endi kino haqida ma'lumot kiriting:", reply_markup=admin_back_menu)


@dp.message_handler(F.AdminFilter(), state=KinoCreation.waiting_for_kino_info)
async def kino_info(message: types.Message, state: FSMContext):
    await state.update_data(kino_info=message.text)
    await KinoCreation.next()
    await message.answer("Endi kinoni yuklang:", reply_markup=admin_back_menu)


@dp.message_handler(F.AdminFilter(), content_types=['video'], state=KinoCreation.waiting_for_kino)
async def kino_file(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    channel_id = private_channel
    tizer_file_id = user_data['tizerFile_id']
    sent_message = await message.bot.send_video(chat_id=channel_id, video=message.video.file_id)
    kino_size = format_size(sent_message.video.file_size)
    kod = generate_kino_kod()
    caption_tizer = (f"<b>Aynan shu kinoni to'liq xolda \nbotimizga joyladik</b>\n\n"
                     f"ℹ️ {user_data['kino_info']}\n\n"
                     f"<i>Filmni yuklab olish uchun botimizga kiring va kodni kiriting</i>\n\n"
                     f"🔑 Kod: <b><i>{kod}</i></b>\n\n"
                     f"👉{asosiy_channel}")
    caption_tizer1 = (f"🎬 Nomi: {user_data['kino_nomi']}\n"
                     f"ℹ️ Kino haqida: {user_data['kino_info']}\n"
                      f"💾 Hajmi: {kino_size}\n"
                     f"🔑 Kod: {kod}\n"
                     f"🔗 Kinoni ko'rish: <a href='{asosiy_bot}?start=havola_click_{kod}'>Havola</a>\n\n"
                     f"👉{asosiy_channel}")
    type = user_data['tizer_type']
    if type == 'video':
        asosiy_tizer_message_id = await message.bot.send_video(chat_id=asosiy_channel, video=tizer_file_id, caption=caption_tizer, reply_markup=move_download(kod))
        tizer_message = await message.bot.send_video(chat_id=channel_id, video=tizer_file_id, caption=caption_tizer1)
    else:
        asosiy_tizer_message_id = await message.bot.send_photo(chat_id=asosiy_channel, photo=tizer_file_id, caption=caption_tizer, reply_markup=move_download(kod))
        tizer_message = await message.bot.send_photo(chat_id=channel_id, photo=tizer_file_id, caption=caption_tizer1)
    message_id = sent_message.message_id
    await state.update_data(kinoMessage_id=message_id, kino_hajmi=kino_size)
    await create_kino(
        kod=kod,
        tizer_message_id=tizer_message.message_id,
        asosiy_tizer_message_id=asosiy_tizer_message_id.message_id,
        kino_message_id=message_id,
        kino_nomi=user_data['kino_nomi'],
        kino_info=user_data['kino_info'],
        kino_hajmi=kino_size
    )
    kinolar = await get_all_kinolar()
    await state.finish()
    await message.answer(f"Kino muvaffaqiyatli qo'shildi: <b>{user_data['kino_nomi']} ({kino_size})</b> 🎉",
                         reply_markup=create_kino_keyboard(kinolar=kinolar))

@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data and c.data.startswith('kino_'), state="*")
async def view_kino_details(callback_query: types.CallbackQuery):
    kino_kod = int(callback_query.data.split('_')[-1])
    kino = await get_kino_by_kod(kino_kod)
    formatted_size = kino.kino_hajmi
    text = f"<b>🎬 Nomi:</b> {kino.kino_nomi}\n\n📄 <b>Kino haqida:</b> {kino.kino_info}\n\n<b>💾 Hajmi:</b> {formatted_size}"
    keyboard = kino_details_keyboard(kino)
    await callback_query.message.edit_text(text, reply_markup=keyboard)

@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('name_kino_'), state="*")
async def prompt_new_kino_name(callback_query: types.CallbackQuery, state: FSMContext):
    kino_kod = int(callback_query.data.split('_')[-1])
    await KinoCreation_Edit.waiting_for_kino_nomi.set()
    await state.set_data({'kino_kod': kino_kod})
    await callback_query.message.edit_text("Shu kino uchun yangi nom kiriting:")


@dp.message_handler(F.AdminFilter(), state=KinoCreation_Edit.waiting_for_kino_nomi)
async def process_kino_name_update(message: types.Message, state: FSMContext):
    new_name = message.text
    user_data = await state.get_data()
    kino_kod = user_data['kino_kod']
    try:
        updated_kino = await update_kino(kino_kod, kino_nomi=new_name)
        if not updated_kino:
            await message.answer("❌ Kino topilmadi.")
            await state.finish()
            return
        kino = await get_kino_by_kod(kino_kod)
        if not kino:
            await message.answer("❌ Kino topilmadi.")
            await state.finish()
            return
        tizerMessage_id = kino.tizerMessage_id
        kino_info = kino.kino_info
        formatted_size = kino.kino_hajmi
        caption_tizer1 = (
            f"🎬 Nomi: {new_name}\n"
            f"ℹ️ Kino haqida: {kino_info}\n"
            f"💾 Hajmi: {formatted_size}\n"
            f"🔑 Kod: {kino.kod}\n"
            f"🔗 Kinoni ko'rish: <a href='{asosiy_bot}?start=havola_click_{kino.kod}'>Havola</a>\n\n"
            f"👉{asosiy_channel}"
        )
        if tizerMessage_id:
            await bot.edit_message_caption(
                chat_id=private_channel,
                message_id=tizerMessage_id,
                caption=caption_tizer1,
                parse_mode="HTML"
            )
        text = f"<b>🎬 Nomi:</b> {new_name}\n\n📄 <b>Kino haqida:</b> {kino_info}\n\n<b>💾 Hajmi:</b> {formatted_size}"
        await message.answer(f"Kino nomi muvaffaqiyatli yangilandi 🎉 \n\n{text}", reply_markup=kino_details_keyboard(kino))

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
    finally:
        await state.finish()

@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('info_kino_'), state="*")
async def prompt_new_kino_info(callback_query: types.CallbackQuery, state: FSMContext):
    kino_kod = int(callback_query.data.split('_')[-1])
    await KinoCreation_Edit.waiting_for_kino_info.set()
    await state.set_data({'kino_kod': kino_kod})
    await callback_query.message.edit_text("Shu kino uchun yangi ma'lumot kiriting:")

@dp.message_handler(F.AdminFilter(), state=KinoCreation_Edit.waiting_for_kino_info)
async def process_kino_info_update(message: types.Message, state: FSMContext):
    new_info = message.text
    user_data = await state.get_data()
    kino_kod = user_data['kino_kod']
    try:
        updated_kino = await update_kino(kino_kod, kino_info=new_info)
        if not updated_kino:
            await message.answer("❌ Kino topilmadi.")
            await state.finish()
            return
        kino = await get_kino_by_kod(kino_kod)
        asosiy_tizer_message_id = kino.asosiy_tizer_message_id
        tizerMessage_id = kino.tizerMessage_id
        kod = kino.kod
        kino_nomi = kino.kino_nomi
        kino_hajmi = kino.kino_hajmi
        caption_tizer = (
            f"<b>Aynan shu kinoni to'liq xolda \nbotimizga joyladik</b>\n\n"
            f"ℹ️ {new_info}\n\n"  
            f"<i>Filmni yuklab olish uchun botimizga kiring va kodni kiriting</i>\n\n"
            f"🔑 Kod: <b><i>{kod}</i></b>\n\n"
            f"👉{asosiy_channel}"
        )
        caption_tizer1 = (
            f"🎬 Nomi: {kino_nomi}\n"
            f"ℹ️ Kino haqida: {new_info}\n"  # Yangilangan info
            f"💾 Hajmi: {kino_hajmi}\n"
            f"🔑 Kod: {kod}\n"
            f"🔗 Kinoni ko'rish: <a href='{asosiy_bot}?start=havola_click_{kod}'>Havola</a>\n\n"
            f"👉{asosiy_channel}"
        )
        formatted_size = kino.kino_hajmi
        text = f"<b>🎬 Nomi:</b> {kino.kino_nomi}\n\n📄 <b>Kino haqida:</b> {kino.kino_info}\n\n<b>💾 Hajmi:</b> {formatted_size}"
        if asosiy_tizer_message_id:
            await bot.edit_message_caption(
                chat_id=asosiy_channel,
                message_id=asosiy_tizer_message_id,
                caption=caption_tizer,
                reply_markup=move_download(kod),
                parse_mode="HTML"
            )
            await bot.edit_message_caption(
                chat_id=private_channel,
                message_id=tizerMessage_id,
                caption=caption_tizer1,
                parse_mode="HTML"
            )
            await message.answer(f"Kino haqida ma'lumot yangilandi 🎉\n<b>{new_info}</b>\n\n{text}", reply_markup=kino_details_keyboard(kino))
        else:
            await message.answer("❗️ Tizer ma'lumotlari topilmadi.")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
    finally:
        await state.finish()

@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('delete_kino_'), state="*")
async def ask_delete_kino_confirmation(callback_query: types.CallbackQuery):
    kino_kod = int(callback_query.data.split('_')[-1])
    kino = await get_kino_by_kod(kino_kod)
    if not kino:
        await callback_query.message.answer("Kino topilmadi yoki allaqachon o'chirilgan.")
        return
    keyboard = create_kino_confirmation_keyboard(kino_kod)

    await callback_query.message.edit_text(
        f"Kino o'chiriladi: <b>{kino.kino_nomi}</b>\n\nRostdan o'chirmoqchimisiz?",
        reply_markup=keyboard
    )
    await callback_query.answer()
@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data.startswith('confirm_kino_delete_'), state="*")
async def delete_kino(callback_query: types.CallbackQuery):
    kino_kod = int(callback_query.data.split('_')[-1])
    try:
        kino = await get_kino_by_kod(kino_kod)
        if not kino:
            await callback_query.message.answer("Kino topilmadi yoki allaqachon o'chirilgan.")
            return

        channel_id = private_channel
        main_channel_id = asosiy_channel

        if kino.tizerMessage_id:
            await callback_query.bot.delete_message(channel_id, kino.tizerMessage_id)
        if kino.kinoMessage_id:
            await callback_query.bot.delete_message(channel_id, kino.kinoMessage_id)
        if kino.asosiy_tizer_message_id:
            await callback_query.bot.delete_message(main_channel_id, kino.asosiy_tizer_message_id)

        deleted = await delete_kino_by_kod(kino_kod)

        if deleted:
            kinolar = await get_all_kinolar()
            keyboard = create_kino_keyboard(kinolar)
            delete_message = f"Kino o'chirildi: <b>{kino.kino_nomi} 🎉</b>"
            if not kinolar:
                delete_message += "\n\n❗️ Bazada kino qolmadi"
                keyboard = create_kino_keyboard(kinolar=kinolar)
            await callback_query.message.edit_text(delete_message, reply_markup=keyboard)
        else:
            await callback_query.message.answer("Kino o'chirishda xatolik yuz berdi.")
    except Exception as e:
        await callback_query.message.answer(f"Kino o'chirishda xato: {str(e)}")
    await callback_query.answer()
@dp.callback_query_handler(F.AdminFilter(), lambda c: c.data == "cancel_kino_delete", state="*")
async def cancel_kino_delete(callback_query: types.CallbackQuery):
    kinolar = await get_all_kinolar()
    await callback_query.message.edit_text(
        "Kino o'chirish bekor qilindi.",
        reply_markup=create_kino_keyboard(kinolar=kinolar)
    )
    await callback_query.answer()

