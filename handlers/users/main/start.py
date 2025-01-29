from typing import Union
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.texts import text, button
from keyboards.inline.inline_user import create_main_menu_keyboard, create_action_keyboard, all_serial, \
 create_serial_parts_keyboard1
from loader import dp, bot
from states.user import KinoQuery
from utils.database.functions.f_kino import kino_exists, get_tizer_message_id_by_tizer_id
from utils.database.functions.f_serial import fetch_all_serials, fetch_serial_by_id, fetch_serial_parts, \
    fetch_serial_parts1
from utils.database.functions.f_user import create_user, get_user
from data.config import private_channel, asosiy_bot, asosiy_channel
@dp.message_handler(lambda message: message.text.isdigit())
async def receive_kino_code(message: types.Message):
    kino_kod = int(message.text)
    tizer_message_id = await get_tizer_message_id_by_tizer_id(kino_kod)
    if tizer_message_id:
        await message.bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=private_channel,
            message_id=tizer_message_id,
            reply_markup=await create_action_keyboard(kino_kod)
        )
    else:
        await message.answer("Kiritilgan kino kodiga mos kino topilmadi.")

@dp.message_handler(commands=['start'], state="*")
@dp.message_handler(text=button("user_back"), state="*")
async def user_start_handler(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name
    user = await get_user(user_id)
    if not user:
        await create_user(user_id=user_id, username=username, fullname=fullname)
    if isinstance(message, types.Message):
        if message.text.startswith('/start havola_click_'):
            args = message.get_args()
            tezer_id = args.split('_')[2]
            print("Tizer id:", int(tezer_id))
            tizer_message_id = await get_tizer_message_id_by_tizer_id(int(tezer_id))
            print("Tizer message id:", tizer_message_id)
            print("Doston jo'ram>>>>>>>>>>", int(tezer_id))
            if tizer_message_id:
                print("33333")
                print(await create_action_keyboard(int(tezer_id)))
                await bot.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=private_channel,
                    message_id=tizer_message_id,
                    reply_markup=await create_action_keyboard(int(tezer_id))
                )
            print("asosiy bot: kino mavjud emas")
        elif message.text.startswith('/start'):
            await message.answer("Assalomu alaykum quyidagilrdan birini tanlang:", reply_markup=create_main_menu_keyboard())
        else:
            args = message.get_args()
            tizer_message_id = await get_tizer_message_id_by_tizer_id(int(args))
            if tizer_message_id:
                await bot.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=private_channel,
                    message_id=tizer_message_id,
                    reply_markup=create_action_keyboard(int(args))
                )
@dp.callback_query_handler(text="user_kino", state="*")
async def ask_for_kino_kod(callback_query: types.CallbackQuery):
    await KinoQuery.waiting_for_kino_kod.set()
    await callback_query.message.edit_text("Iltimos, kino kodini kiriting:")

@dp.message_handler(state=KinoQuery.waiting_for_kino_kod)
async def process_kino_kod(message: types.Message, state: FSMContext):
    kino_kod = int(message.text)
    exists, kino = await kino_exists(kino_kod)
    if exists:
        chat_id = message.chat.id
        caption_tizer = (f"📛 Nomi: {kino.kino_nomi}\n"
                         f"ℹ️ Kino haqida: {kino.kino_info}\n"
                         f"💾 Hajmi: {kino.kino_hajmi}\n"
                         f"🔑 Kod: <b><i>{kino.kod}</i></b>\n"
                         f"🔗 Bot: {asosiy_bot}\n\n"
                         f"👉{asosiy_channel}")
        action_keyboard = create_action_keyboard(kino.kinoMessage_id)
        await message.bot.copy_message(chat_id, private_channel, kino.tizerMessage_id, caption=caption_tizer, reply_markup=action_keyboard)
    else:
        await message.answer("Kino topilmadi boshqa kod kiriting.")
    await state.finish()

@dp.callback_query_handler(text="user_serial", state="*")
async def handle_serial_button(callback_query: types.CallbackQuery):
    serials = await fetch_all_serials()
    if serials:
        keyboard = await all_serial(serials, page=0)
        await callback_query.message.edit_text("🎞 Seriallar👇", reply_markup=keyboard)
    else:
        await callback_query.message.edit_text("❗️ Hozirda serial mavjud emas.")
    await callback_query.answer()

@dp.callback_query_handler(text_startswith="slide_serial_", state="*")
async def slide_serials(callback_query: types.CallbackQuery):
    data = callback_query.data.split("_")
    page = int(data[-1])
    serials = await fetch_all_serials()
    keyboard = await all_serial(serials, page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()
@dp.callback_query_handler(text_startswith="serialUser_", state="*")
async def show_serial_parts(callback_query: types.CallbackQuery):
    serial_id = int(callback_query.data.split("_")[1])
    serial = await fetch_serial_by_id(serial_id)
    parts = await fetch_serial_parts(serial_id)
    keyboard = await create_serial_parts_keyboard1(serial_id, parts, page=0)
    if parts:
        await callback_query.message.edit_text(
            text=f"<b>🎞 {serial.serial_nomi}</b> serialiga tegishli qismlar:",
            reply_markup=keyboard
        )
    else:
        await callback_query.message.edit_text(
            f"<b>❗️ {serial.serial_nomi}</b> serialiga hali qismlar qo'shilmagan.",
            reply_markup=keyboard
        )
@dp.callback_query_handler(text_startswith="slideUser_parts_", state="*")
async def slide_serial_parts(callback_query: types.CallbackQuery):
    data = callback_query.data.split("_")
    serial_id = int(data[2])
    page = int(data[3])
    parts = await fetch_serial_parts(serial_id)
    keyboard = await create_serial_parts_keyboard1(serial_id, parts, page)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("userQismprev_") or c.data.startswith("userQismnext_"), state="*")
async def change_page_callback(query: types.CallbackQuery):
    data_parts = query.data.split("_")

    if len(data_parts) == 3:
        _, kino_id, page = data_parts
        kino_id = int(kino_id)
        page = int(page)
        keyboard = await create_action_keyboard(kino_id, page)
        await query.message.edit_reply_markup(reply_markup=keyboard)
    else:
        await query.answer("Xatolik yuz berdi: noto‘g‘ri format", show_alert=True)

    await query.answer()


@dp.callback_query_handler(text="user_back", state="*")
async def start_handler(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.edit_text("Assalomu alaykum, quyidagilardan birini tanlang:", reply_markup=create_main_menu_keyboard())
    await query.answer()