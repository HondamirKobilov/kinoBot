from aiogram.types import (
    InlineKeyboardMarkup as IKM,
    InlineKeyboardButton as IKB
)

from data.config import channels_manager
from data.texts import button
from utils.database.functions.f_serial import count_serial_parts, fetch_serial_parts


def inline_admin_keyboards(*args):
    return [IKB(text=button(i), callback_data=i) for i in args]

admin_main_menu = IKM(
    row_width=1,
    inline_keyboard=[
        inline_admin_keyboards("admin_send_message"),
        inline_admin_keyboards("admin_statistics"),
        inline_admin_keyboards("admin_manage_channels"),
        inline_admin_keyboards("admin_kinolar"),
        inline_admin_keyboards("admin_seriallar")
    ]
)

admin_back_menu = IKM(
    row_width=1,
    inline_keyboard=[
        inline_admin_keyboards("admin_back")
    ]
)


def channels_menu():
    keyboard = IKM(row_width=1)
    channels = channels_manager.get_channels()
    for i, channel in enumerate(channels, start=1):
        keyboard.insert(IKB(f"{i}. {channel['title']}", callback_data=f"admin_edit_{channel['id']}"))

    keyboard.add(IKB(button("admin_add_channel"), callback_data="admin_add_channel"))
    keyboard.add(IKB(button("admin_back"), callback_data="admin_back"))
    return keyboard


def edit_channel_menu(channel_id):
    keyboard = IKM(row_width=2)
    keyboard.insert(IKB(button("admin_edit"), callback_data=f"admin_modify_{channel_id}"))
    keyboard.insert(IKB(button("admin_delete"), callback_data=f"admin_delete_{channel_id}"))
    keyboard.add(IKB(button("admin_back"), callback_data="admin_back_to_channels"))
    return keyboard


def create_kino_keyboard(kinolar):
    keyboard = IKM(row_width=1)
    if kinolar:
        for kino in kinolar:
            button = IKB(kino.kino_nomi, callback_data=f"kino_{kino.kod}")
            keyboard.add(button)
    add_kino_button = IKB("➕ Kino qo'shish", callback_data="add_kino")
    keyboard.add(add_kino_button)
    back_button = IKB("⬅️ Ortga", callback_data="admin_back")
    keyboard.add(back_button)
    return keyboard

def kino_details_keyboard(kino):
    keyboard = IKM(row_width=2)
    kino_nomi_button = IKB(f"🎬 Nomi", callback_data=f"name_kino_{kino.kod}")
    kino_info_button = IKB(f"📄 Info", callback_data=f"info_kino_{kino.kod}")
    delete_button = IKB("🗑 O'chirish", callback_data=f"delete_kino_{kino.kod}")
    back_button = IKB("🔙 Ortga", callback_data="admin_back")
    keyboard.row(kino_nomi_button, kino_info_button)
    keyboard.row(delete_button, back_button)
    return keyboard
SERIALS_PER_PAGE = 10
async def create_serials_keyboard(serials, page):
    keyboard = IKM(row_width=1)
    total_pages = (len(serials) - 1) // SERIALS_PER_PAGE + 1
    start_index = page * SERIALS_PER_PAGE
    end_index = start_index + SERIALS_PER_PAGE
    serials_on_page = serials[start_index:end_index]
    for serial in serials_on_page:
        qismSoni = await count_serial_parts(serial.serial_id)
        button_text = serial.serial_nomi
        button_callback = f"serial_{serial.serial_id}"
        keyboard.add(IKB(text=f"{button_text} ({qismSoni})", callback_data=button_callback))
    if total_pages > 1:
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(IKB("⬅️ Ortga", callback_data=f"admin_slide_serial_{page - 1}"))
        if page < total_pages - 1:
            navigation_buttons.append(IKB("➡️ Oldinga", callback_data=f"admin_slide_serial_{page + 1}"))
        keyboard.row(*navigation_buttons)
    add_serial_button = IKB("➕ Serial qo'shish", callback_data="add_serial")
    keyboard.add(add_serial_button)
    back_button = IKB("🔙 Ortga", callback_data="admin_back")
    keyboard.add(back_button)
    return keyboard

SERIAL_PARTS_PER_PAGE = 10
async def create_serial_parts_keyboard(serial_id, page):
    keyboard = IKM(row_width=1)
    parts = await fetch_serial_parts(serial_id)
    total_pages = (len(parts) - 1) // SERIAL_PARTS_PER_PAGE + 1
    start_index = page * SERIAL_PARTS_PER_PAGE
    end_index = start_index + SERIAL_PARTS_PER_PAGE
    parts_on_page = parts[start_index:end_index]
    for part in parts_on_page:
        button_text = part.serial_nomi
        button_callback = f"part_{part.id}"
        keyboard.add(IKB(text=button_text, callback_data=button_callback))
    if total_pages > 1:
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(IKB("⬅️ Ortga", callback_data=f"slide_parts_{serial_id}_{page - 1}"))
        if page < total_pages - 1:
            navigation_buttons.append(IKB("➡️ Oldinga", callback_data=f"slide_parts_{serial_id}_{page + 1}"))
        keyboard.row(*navigation_buttons)
    add_part_button = IKB("➕ Qism qo'shish", callback_data=f"add_part_{serial_id}")
    name_edit_button = IKB("✏️ Name edit", callback_data=f"edit_serialname_{serial_id}")
    delete_serial_button = IKB("🗑 Serialni o'chirish", callback_data=f"delete_serial_{serial_id}")
    back_button = IKB("🔙 Ortga", callback_data="admin_back")
    keyboard.add(add_part_button, name_edit_button, delete_serial_button)
    keyboard.add(back_button)
    return keyboard

def create_confirmation_keyboard(serial_id: int) -> IKM:
    keyboard = IKM(row_width=2)
    keyboard.add(
        IKB(text="✅ Ha", callback_data=f"confirmserial_delete_{serial_id}"),
        IKB(text="❌ Yo'q", callback_data="cancelserial_delete")
    )
    return keyboard
def create_kino_confirmation_keyboard(kino_kod: int) -> IKM:
    keyboard = IKM(row_width=2)
    keyboard.add(
        IKB(text="✅ Ha", callback_data=f"confirm_kino_delete_{kino_kod}"),
        IKB(text="❌ Yo'q", callback_data="cancel_kino_delete")
    )
    return keyboard

def create_part_action_keyboard(part_id: int) -> IKM:

    keyboard = IKM(row_width=2)
    keyboard.add(
        IKB(text="📝 Nomi", callback_data=f"edit_part_name_{part_id}"),
        IKB(text="ℹ️ Info", callback_data=f"edit_part_info_{part_id}"),
        IKB(text="🗑 O'chirish", callback_data=f"delete_part_{part_id}")
    )
    keyboard.add(IKB(text="🔙 Ortga", callback_data="admin_back"))
    return keyboard


def create_confirmation_keyboard_part(part_id: int) -> IKM:
    keyboard = IKM(row_width=2)
    keyboard.add(
        IKB(text="✅ Ha", callback_data=f"partt_confirm_delete_{part_id}"),
        IKB(text="❌ Yo'q", callback_data=f"partt_cancel_delete_{part_id}")
    )
    return keyboard

def create_part_action_buttons(part_id: int, serial_id: int):
    keyboard = IKM(row_width=2)
    keyboard.add(
        IKB("🎞 Nomi", callback_data=f"edit_part_name_{part_id}"),
        IKB("📄 Info", callback_data=f"edit_part_info_{part_id}"),
    )
    keyboard.add(
        IKB("🗑 O'chirish", callback_data=f"delete_part_{part_id}"),
        IKB("🔙 Ortga", callback_data=f"admin_back"),
    )
    return keyboard
