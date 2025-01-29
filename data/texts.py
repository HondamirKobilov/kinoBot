_texts = {
    "admin_new_user_to_channel": """<b>🆕 Yangi foydalanuvchi:</b>
<b>Ismi:</b> 👉 <a href='tg://user?id={user_id}'>{fullname}</a>
<b>ID:</b> {user_id}
<b>Username:</b> @{username}

{is_premium}

{created_at}""",
    "admin_start": """⚡️ Assalomu alaykum, Hurmatli {fullname}
<a href=\"https://telegra.ph/file/aa08d65c33a2664e1abe8.jpg\"> </a>
Marhamat siz uchun admin paneli quyidagilar""",
    "admin_statistics": """📊┌ STATISTIKA
👥├ A`zolar: {all_users} ta
👥├ Faol a'zolar: {active_users} ta
👥├ Bugun kirganlar: {today_users} ta
👥├ Bugun ishlatganlar: {daily_users} ta
👥├ Premium obunachilar: {premium_users} ta""",
    "admin_started_sending_messages": "<b>Xabar tarqatish boshlandi!</b>",
    "admin_message_distribution_completed": """<b>Xabarni tarqatish tugallandi.</b>

<b>Jami yuborilgan xabarlar:</b> <code>{total_sent}</code>
<b>Jami bloklangan foydalanuvchilar:</b> <code>{total_blocked}</code>""",
    "admin_reply_to_send_command": """<b>Biror bir xabarga reply qilib yozing
(<code>/send</code>)</b>""",
    "admin_send_message_instruction": """<a href='telegra.ph/file/31c6e3fd53055c1388dac.jpg'> </a>Istalgan xabarni forward yoki oddiy yuboring va yuborgan xabaringizga <b><u>reply</u></b> qilib,
<code>/send</code> buyrug'ini yuboring!
Batafsil quyida:""",
    "admin_channel_added": """✅ <b>Kanal qo'shildi: 
{channel_name}</b> (ID: {channel_id})""",
    "admin_manage_channels_intro": "<b>💠 Kanallar boshqaruvi:</b>",
    "admin_enter_new_channel_id": "<b>Iltimos, yangi kanalning IDsini kiriting:</b>",
    "admin_enter_channel_name": "<b>Endi kanal nomini kiriting:</b>",
    "admin_channel_not_found": "🚫 Kanal topilmadi.",
    "admin_channel_edit_prompt": """<b>📢 Kanal: {channel_title}</b>
Nima qilmoqchisiz?""",
    "admin_channel_deleted": "🗑 Kanal o'chirildi.",
    "admin_enter_new_channel_id_for_modification": "<b>Iltimos, kanalning yangi ID'sini kiriting:</b>",
    "admin_enter_new_channel_name": "<b>Endi yangi kanal nomini kiriting:</b>",
    "admin_channel_modified": """<b>🔄 Kanal yangilandi:</b>
 {new_channel_name} (ID: {new_channel_id})
Nima qilmoqchisiz?""",
    "user_register_language": "🇺🇿 O'zingizga kerakli tilni tanlang:"
                              "\n\n🇷🇺 Выберите язык, который вы хотите:",
    "user_subscribe_request": "Botni ishlatish uchun quyidagi kanalga obuna bo'lish talab qilinadi!",
    "user_please_wait": "Iltimos biroz kutib turing...",
    "user_start": """<b>🤝 Assalomu alaykum, Ziyotest botiga xush kelibsiz!
🔎 Ushbu bot yordamida siz turli testlarni yaratishingiz va ulardan foydalanishingiz mumkin.
📋 Diqqat: Bot yaqinda ishga tushganligi sababli, test yaratish jarayonida sabrli bo'lishingizni so'raymiz. Kelgusida xizmatlarimizni yanada qulaylashtirish uchun tinimsiz ishlayapmiz.</b>""",
    "user_default_share": """<b>Do'stim, men 2021, 2022, 2023-yillardagi o'tish ballarini topdim</b>

🔗 Ushbu havola orqali o'ting va o'tgan yildagi ballarni bilib oling!

👉 <b><a href='{PRE_USERNAME}{user_id}'>@{USERNAME}</a></b>""",
    "user_click_me": "Ustiga bosing!",
    "user_select_subject": "<b>🔰 Fanlarni tanlang:</b>",
    "user_select_etype": "<b>🔰 Ta'lim shaklini tanlang:</b>",
    "user_select_language": "<b>🇺🇿 Ta'lim tilini tanlang:</b>",
    "user_select_institutes": "<b>🏢 OTMni tanlang:</b>",
    "user_select_regions": "<b>📍 Hududni tanlang:</b>",
    "user_select_directions": "<b>📚 Ta'lim yo'nalishini tanlang:</b>",
    "user_select_kontrakt": "<b>O'quv turini tanlang 👇</b>",
    "user_select_ball": "<b>Saralash uchun ballni kiriting:</b>",
    "user_select_year": "<b>O'quv yilini tanlang:</b>",
    "user_nodata": "<b>🤷🏻‍♂️ Bunday ma'lumot yo'q</b>",
    "user_inline_query": "<b>Tezkor qidiruvdan foydalaning...</b>"
}

_buttons = {
    "admin_send_message": "📤 Xabar yuborish",
    "admin_statistics": "👤 Foydalanuvchilar soni",
    "info_user_admin": "ℹ️ Foydalanuvchilar ma'lumotlari",
    "admin_kinolar": "📽 Kinolar",
    "admin_seriallar": "🎬 Seriallar",
    "admin_school": "🏫 Maktablar",
    "admin_bot_homiy": "🔶 Homiy",
    "admin_test": "📄 Test",
    "admin_fanlar": "📚 Fanlar",
    "admin_admin_add": "👥 Admin qo'shish",
    "user_back_edit": "🔙 Ortga",
    "admin_direction_add": "➕ Yo'nalish qo'shish",
    "admin_checked_direction": "✅ Tasdiqlash",
    "admin_klinika_edit": "📝 Tahrirlash",
    "admin_klinika_delete": "❌ Delete",
    "admin_manage_channels": "⚙️ Kanallar boshqaruvi",
    "admin_add_channel": "🆕 Yangi kanal qo'shish",
    "admin_back": "🔙 Ortga",
    "admin_delete": "❌ O'chirish",
    "admin_edit": "✏️ Tahrirlash",
    "user_check_subscribe": "✅ Obunani tekshirish",
    "user_share": "♻️ Do'stlarga ulashish",
    "user_back": "🔙 Ortga",
    "user_home": "🏠 Bosh menyu",
    "user_inline_query": "🔎 Qidiruv",
    "user_default_konkurs": "🏆 Konkursga qatnashish",
    "user_default_test": "📝 Test ishlash",
    "user_name_edit": "👤Isimni o'zgartirish",
    "user_region_edit": "🌍Hududimni o'zgartirish",
    "user_phone_edit": "☎️Telefon raqamimni o'zgartirish",
    "user_back_edit": "🔙 Ortga"
}


def text(key):
    return _texts[key]


def button(key):
    return _buttons[key]
