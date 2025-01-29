from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("dasturchi", "👨🏼‍💻 Xondamir\n ☎️ 997796202 "),
        ]
    )
