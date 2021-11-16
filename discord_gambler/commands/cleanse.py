from discord.ext import commands
from decouple import config
from discord_gambler import _coinflip_channel
import os


class CleanseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cleanse")
    async def on_cleanse_command(self, ctx):
        if ctx.channel.name == _coinflip_channel:
            print("Cleaning up coinflip channel...")
            for message in await ctx.channel.history(limit=100).flatten():
                await message.delete()
