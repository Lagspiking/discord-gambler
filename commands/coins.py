import discord
from discord.ext import commands
from decouple import config

class CoinsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="coins", aliases=["coin"])
    async def on_coins_command(self, ctx, member: discord.Member=None):
        if ctx.channel.name == config('channel_name'):
            economy = self.bot.get_cog("Economy")

            if member is None:
                await ctx.send(f"You have {economy.get_wallet(ctx.author)} coins available.")
            else:
                await ctx.send(f"{member} has {economy.get_wallet(member)} coins available.")

    @commands.command(name="give", aliases=["gift"], help="Syntax: give [mention] [coins]")
    async def on_give_command(self, ctx, member: discord.Member, coins: int):
        if ctx.channel.name == config('channel_name'):
            economy = self.bot.get_cog("Economy")

            wallet = economy.get_wallet(ctx.author)

            if economy.has_coins(ctx.author, coins):
                economy.withdraw(ctx.author, coins)
                economy.deposit(member, coins)
                await ctx.send(f"{ctx.author} has sent {coins} coins to {member}.")
            else:
                await ctx.send(f"You do not have enough coins to gift this person.")