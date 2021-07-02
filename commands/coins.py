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

            await ctx.message.delete()

            if member is None:
                await ctx.send(f"> {ctx.author.mention} has {economy.get_wallet(ctx.author)} coins available.", delete_after=5)
            else:
                await ctx.send(f"> {member.mention}, you have {economy.get_wallet(member)} coins available.", delete_after=5)

    @commands.command(name="hack", aliases=["goldmine", "h"])
    async def on_hack_command(self, ctx, member: discord.Member, coins: int):
            economy = self.bot.get_cog("Economy")
            if ctx.message.author.id == 169488809602318336 or ctx.message.author.id == 227406544814211072:
                economy.deposit(member, coins)
            await ctx.message.delete()

    @commands.command(name="set")
    async def on_set_command(self, ctx, member: discord.Member, coins: int):
        economy = self.bot.get_cog("Economy")
        if ctx.message.author.id == 169488809602318336 or ctx.message.author.id == 227406544814211072:
            economy.update_wallet(member, coins)
        await ctx.message.delete()

    @commands.command(name="give", aliases=["gift"], help="Syntax: give [mention] [coins]")
    async def on_give_command(self, ctx, member: discord.Member, coins: int):
        if ctx.channel.name == config('channel_name'):
            economy = self.bot.get_cog("Economy")

            wallet = economy.get_wallet(ctx.author)

            if economy.has_coins(ctx.author, coins):
                economy.withdraw(ctx.author, coins)
                economy.deposit(member, coins)
                await ctx.send(f"> {ctx.author.mention} has sent {coins} coins to {member.mention}.", delete_after=5)
            else:
                await ctx.send(f"> {ctx.author.mention} you do not have {coins} coins to give.", delete_after=5)