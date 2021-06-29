from discord.ext import commands

class JackpotCog(commands.Cog, name = "Jackpot"):

    def __init__(self, bot):
        self._bot = bot