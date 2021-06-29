from discord.ext import commands

class CoinsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="coins")
    async def on_coins_command(self, ctx):
        economy = self.bot.get_cog("Economy")
        await ctx.send(f"You have {await economy.get_wallet(ctx.author)} coins available.")