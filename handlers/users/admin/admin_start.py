# from aiogram import types
# from aiogram.dispatcher import FSMContext
#
# from filters import F
#
# from keyboards.inline.inline_user import create_main_menu_keyboard
# from loader import dp
# @dp.message_handler(F.AdminFilter(), commands=['start'], state='*')
# async def start_handler(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer("Assalomu alaykum quyidagilrdan birini tanlang:", reply_markup=create_main_menu_keyboard())
#
#
#
#
