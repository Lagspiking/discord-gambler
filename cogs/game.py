import discord
from discord.ext import commands
import typing

class GameCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "create")
    async def on_create_coinflip_command(self, ctx, coins: int):
        coinflip = self.bot.get_cog("Coinflip")
        await coinflip.create_coinflip(ctx.author, coins)

    @commands.command(name = "join")
    async def on_join_coinflip_command(self, ctx, member: discord.Member):
        coinflip = self.bot.get_cog("Coinflip")
        await coinflip.join_coinflip(member, ctx.author)