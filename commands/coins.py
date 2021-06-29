import discord
from discord.ext import commands

class CoinsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="coins", aliases=["coin"])
    async def on_coins_command(self, ctx, member: discord.Member=None):
        economy = self.bot.get_cog("Economy")

        if member is None:
            await ctx.send(f"You have {await economy.get_wallet(ctx.author)} coins available.")
        else:
            await ctx.send(f"{member} has {await economy.get_wallet(ctx.author)} coins available.")