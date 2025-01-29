from aiogram import types
from data.config import private_channel
from loader import dp2, bot2
from utils.database.functions import f_kino, f_serial
@dp2.message_handler(commands=['start'], state='*')
async def bot_start_handler(message: types.Message):
    if message.text.startswith('/start kino_'):
        encoded_id = message.text.replace('/start kino_', "")
        if encoded_id:
            kino = await f_kino.get_kino_by_kod(encoded_id)
            if kino:
                kino_message_id = kino.kinoMessage_id
                await bot2.copy_message(
                    chat_id=message.from_user.id,
                    from_chat_id=private_channel,
                    message_id=kino_message_id
                )
            else:
                await message.answer("Kino topilmadi.")
        else:
            await message.answer("Kino topilmadi.")
    elif message.text.startswith('/start serial_'):
        encoded_id = message.text.replace('/start serial_', "")
        if encoded_id:
            kino = await f_serial.get_part_by_id1(int(encoded_id))
            if kino:
                kino_message_id = kino.kino_message_id
                await bot2.copy_message(
                    chat_id=message.from_user.id,
                    from_chat_id=private_channel,
                    message_id=kino_message_id
                )
            else:
                await message.answer("Qism topilmadi.")
        else:
            await message.answer("Qism topilmadi.")
    else:
        await message.answer("Xush kelibsiz!")
