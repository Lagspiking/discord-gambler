import discord
from discord.ext import commands

class ChannelCog(commands.Cog, name = "Channel"):

    def __init__(self, bot):
        self._bot = bot