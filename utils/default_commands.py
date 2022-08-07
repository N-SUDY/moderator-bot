async def set_default_commands(dp):
    from load import types
    await dp.bot.set_my_commands([
        types.BotCommand("start","Start bot"),
        types.BotCommand("help","Help")
    ])
