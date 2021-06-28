from commands.command import Command

class LeaderboardsCommand(Command):
    def __init__(self, commandText):
        super().__init__(commandText)
    
    async def on_message(self, message):
        await message.channel.send("Hello World!")