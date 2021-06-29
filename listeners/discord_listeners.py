import discord
from discord.ext import commands
from decouple import config

#https://discordpy.readthedocs.io/en/stable/api.html#event-reference
class DiscordListeners(commands.Cog):
    
    def __init__(self, bot):
        self._bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        pass