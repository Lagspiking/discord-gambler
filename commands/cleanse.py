from discord.ext import commands

class CleanseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="cleanse")
    async def on_cleanse_command(self, ctx):
        for message in ctx.channel.history(limit=100):
            message.delete()