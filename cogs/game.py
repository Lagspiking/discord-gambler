import discord
from discord.ext import commands
import typing

class GameCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "create")
    async def on_create_coinflip_command(self, ctx, coins: int):
        economy = self.bot.get_cog("Economy")
        coinflip = self.bot.get_cog("Coinflip")

        await economy.withdraw_coins(ctx, ctx.author, coins)
        await coinflip.create_coinflip(ctx, ctx.author, coins)

    @commands.command(name = "join")
    async def on_join_coinflip_command(self, ctx, member: discord.Member):
        economy = self.bot.get_cog("Economy")
        coinflip = self.bot.get_cog("Coinflip")

        game = await coinflip.get_coinflip_game(member)

        if game is not None:
            await economy.withdraw_coins(ctx, ctx.author, await game.get_coins())
            await coinflip.join_coinflip(ctx, member, ctx.author)