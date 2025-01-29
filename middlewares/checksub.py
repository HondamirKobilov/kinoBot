from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardMarkup
from data.config import toshkent_now
from data.texts import text
from middlewares.misc import check_status
from utils.database.functions import f_user

class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        # Foydalanuvchi ID ni aniqlash
        user_id = (
            update.message.from_user.id if update.message
            else update.callback_query.from_user.id if update.callback_query
            else False
        )

        if not user_id:
            return

        # `/start` yoki boshqa specific komandalar uchun ishlamaslik
        if update.message and update.message.text and update.message.text.startswith("/start"):
            return  # Agar /start komandasi bo'lsa, middleware ishlamaydi

        # Foydalanuvchi faoliyatini yangilash
        await f_user.update_user(user_id, updated_at=toshkent_now())

        # Guruh xabarlarini bloklash
        if update.message and "group" in update.message.chat.type:
            raise CancelHandler()

        # Obuna holatini tekshirish
        if update.message:
            status, keyboard = await check_status(user_id)
            if not status:
                await update.message.answer(
                    text("user_subscribe_request"),
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    disable_web_page_preview=True
                )
                raise CancelHandler()

        if update.callback_query and not update.callback_query.data.startswith(("district:", 'region:')):
            status, keyboard = await check_status(user_id)
            if not status:
                try:
                    await update.callback_query.message.edit_text(
                        text("user_subscribe_request"),
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                        disable_web_page_preview=True
                    )
                except:
                    try:
                        await update.callback_query.answer("⚠️ Kanalga a'zo bo'ling", cache_time=0)
                    except:
                        pass
                raise CancelHandler()

