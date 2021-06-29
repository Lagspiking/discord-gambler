from discord.ext import commands

#https://discordpy.readthedocs.io/en/stable/api.html#event-reference
class DiscordListeners(commands.Cog):
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("discord is ready")