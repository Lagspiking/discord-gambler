from discord.ext import commands

#https://discordpy.readthedocs.io/en/stable/api.html#event-reference
class MemberListeners(commands.Cog):
    
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass   