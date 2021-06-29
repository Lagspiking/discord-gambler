import discord
from discord.ext import commands

class CurrencyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="coins")
    async def on_coins_command(self, ctx):
        economy = self.bot.get_cog("Economy")
        await ctx.send(f"You have {await economy.get_wallet(ctx.author)} coins!")

    @commands.command(name="give")
    async def on_give_coins_command(self, ctx, coins: int, member: discord.Member):
        print(f"Giving {coins} to {member.display_name}")
        economy = self.bot.get_cog("Economy")

        if economy is not None:
            await economy.deposit_money(member, coins)

        print(await economy.balance(member))