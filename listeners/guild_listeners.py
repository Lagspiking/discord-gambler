from discord.ext import commands

#https://discordpy.readthedocs.io/en/stable/api.html#event-reference
class GuildListeners(commands.Cog):
    
    def __init__(self, bot):
        self._bot = bot
        
    #Called when a Guild is either created by the Client or when the Client joins a guild.
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        pass