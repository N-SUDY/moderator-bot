async def set_default_commands(bot):
    from load import types
    
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="start", description="Start bot"),
            types.BotCommand(command="help", description="Help")
        ]
    )
