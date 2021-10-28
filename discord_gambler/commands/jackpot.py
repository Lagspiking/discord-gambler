import discord
from discord.ext import commands

class JackpotCommand(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
    