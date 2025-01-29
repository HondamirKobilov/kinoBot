from aiogram.dispatcher.filters.state import State, StatesGroup


class ChannelAdding(StatesGroup):
    waiting_for_channel_id = State()
    waiting_for_channel_name = State()


class ChannelModification(StatesGroup):
    waiting_for_new_id = State()
    waiting_for_new_name = State()


class KinoCreation(StatesGroup):
    waiting_for_tizer = State()
    waiting_for_kino_nomi = State()
    waiting_for_kino_info = State()
    waiting_for_kino = State()


class KinoCreation_Edit(StatesGroup):
    waiting_for_kino_nomi = State()
    waiting_for_kino_info = State()


class SerialCreation(StatesGroup):
    waiting_for_serial_name = State()


class QismCreation(StatesGroup):
    waiting_for_tizer = State()
    waiting_for_kino_nomi = State()
    waiting_for_kino_info = State()
    waiting_for_kino = State()
