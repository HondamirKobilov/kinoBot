from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from data.config import asosiy_bot, yordamchi_bot, kino_kodKey
import hashlib
import base64
from utils.database.functions.f_serial import count_serial_parts, check_kino_id, get_serial_id, get_serial_parts


def create_main_menu_keyboard():
    keyboard = IKM(row_width=2)
    kino_button = IKB(text="🎬 Kino", callback_data="user_kino")
    serial_button = IKB(text="📺 Serial", callback_data="user_serial")
    keyboard.add(kino_button, serial_button)
    return keyboard
def create_back_button():
    keyboard = IKM()
    back_button = IKB(text="Ortga 🔙", callback_data="user_back")
    keyboard.add(back_button)
    return keyboard
def hash_kino_id(kino_id):
    hash_object = hashlib.sha256((str(kino_id) + kino_kodKey).encode())
    hash_digest = hash_object.digest()
    encoded_hash = base64.urlsafe_b64encode(hash_digest).decode('utf-8')
    return encoded_hash


async def create_action_keyboard(kino_id: int, page: int = 1):
    keyboard = IKM()
    kino_or_serial = await check_kino_id(kino_id)
    if kino_or_serial.startswith("kino_"):
        download_url = f"{yordamchi_bot}{kino_or_serial}"
        download_button = IKB("\U0001F4E5 Kino yuklab olish", url=download_url)
        share_button = IKB("\u267B\uFE0F Do'stlarga ulashish",
                           url=f"https://t.me/share/url?url={asosiy_bot}?start=havola_click_{kino_id}")
        back_button = IKB("Ortga \U0001F519", callback_data="back")
        keyboard.add(download_button)
        keyboard.add(share_button)
        keyboard.row(back_button)
    else:
        serial_id = await get_serial_id(kino_id)
        all_parts = await get_serial_parts(serial_id)
        buttons = []
        per_page = 10
        total_parts = len(all_parts)
        if page > (total_parts // per_page) + 1:
            page = 1
        elif page < 1:
            page = (total_parts // per_page) + 1
        start_index = (page - 1) * per_page
        end_index = min(start_index + per_page, total_parts)
        for i, part in enumerate(all_parts[start_index:end_index], start=start_index + 1):
            part_code = part.kod
            download_url = f"{yordamchi_bot}serial_{part_code}"
            buttons.append(IKB(f"{i}", url=download_url))
            if len(buttons) == 5:
                keyboard.row(*buttons)
                buttons = []
        if buttons:
            keyboard.row(*buttons)
        prev_button = IKB("⬅️ Oldingi", callback_data=f"userQismprev_{kino_id}_{page - 1}")
        next_button = IKB("Keyingi ➡️", callback_data=f"userQismnext_{kino_id}_{page + 1}")
        share_button = IKB("\u267B\uFE0F Do'stlarga ulashish",
                           url=f"https://t.me/share/url?url={asosiy_bot}?start=havola_click_{kino_id}")
        back_button = IKB("Ortga 🔙", callback_data="back")
        keyboard.row(prev_button, next_button)
        keyboard.row(share_button)
        keyboard.row(back_button)
    return keyboard


SERIALS_PER_PAGE = 10
async def all_serial(serials, page):
    keyboard = IKM(row_width=1)
    total_pages = (len(serials) - 1) // SERIALS_PER_PAGE + 1
    start_index = page * SERIALS_PER_PAGE
    end_index = start_index + SERIALS_PER_PAGE
    serials_on_page = serials[start_index:end_index]
    for serial in serials_on_page:
        qismSoni = await count_serial_parts(serial.serial_id)
        button_text = serial.serial_nomi
        button_callback = f"serialUser_{serial.serial_id}"
        keyboard.add(IKB(text=f"{button_text} ({qismSoni})", callback_data=button_callback))
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(IKB("⬅️ Ortga", callback_data=f"slide_serial_{page - 1}"))
    if page < total_pages - 1:
        navigation_buttons.append(IKB("➡️ Oldinga", callback_data=f"slide_serial_{page + 1}"))
    if navigation_buttons:
        keyboard.row(*navigation_buttons)
    back_button = IKB("🔙 Ortga", callback_data="user_back")
    keyboard.add(back_button)
    return keyboard

PARTS_PER_PAGE = 10


async def create_serial_parts_keyboard1(serial_id, parts, page):
    keyboard = IKM(row_width=5)
    total_pages = (len(parts) - 1) // PARTS_PER_PAGE + 1

    # Optimallashtirilgan sahifalash
    if page >= total_pages:
        page = 0  # Agar oxirgi slideda bo‘lsa va yana keyingi bosilsa, boshidan boshlanadi
    elif page < 0:
        page = total_pages - 1  # Agar 1-slideda tursa va oldingi bosilsa, oxirgi slidedan boshlanadi

    start_index = page * PARTS_PER_PAGE
    end_index = min(start_index + PARTS_PER_PAGE, len(parts))
    parts_on_page = parts[start_index:end_index]

    row_buttons = []
    for idx, part in enumerate(parts_on_page, start=start_index + 1):
        download_url = f"{yordamchi_bot}serial_{part.kod}"
        row_buttons.append(IKB(text=str(idx), url=download_url))
        if len(row_buttons) == 5:
            keyboard.row(*row_buttons)
            row_buttons = []

    if row_buttons:
        keyboard.row(*row_buttons)

    if total_pages > 1:
        navigation_buttons = []
        navigation_buttons.append(IKB("⬅️ Ortga", callback_data=f"slideUser_parts_{serial_id}_{page - 1}"))
        navigation_buttons.append(IKB("➡️ Oldinga", callback_data=f"slideUser_parts_{serial_id}_{page + 1}"))
        keyboard.row(*navigation_buttons)

    back_button = IKB("🔙 Ortga", callback_data="user_back")
    keyboard.add(back_button)

    return keyboard

def move_download(kod):
    keyboard = IKM(row_width=1)
    button = IKB(text="Kinoni Yuklab olish", url=f"{asosiy_bot}?start=havola_click_{kod}")
    keyboard.add(button)
    return keyboard