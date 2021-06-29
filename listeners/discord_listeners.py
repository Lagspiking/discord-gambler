from discord.ext import commands

#https://discordpy.readthedocs.io/en/stable/api.html#event-reference
class DiscordListeners(commands.Cog):
    
    def __init__(self, bot):
        self._bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("discord is ready")