import discord
from discord.ext import commands
from decouple import config

class LeaderboardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="leader")
    async def on_cleanse_command(self, ctx):
        guild = discord.utils.get(self.bot.guilds, name="$ui$lide")
        bot_channel = discord.utils.get(guild.text_channels, name="gamble-bot")
        economy = self.bot.get_cog("Economy")
        all_wallets = economy.get_all_wallets()
        sorted_wallets = sorted(all_wallets.items(), key=lambda x: x[1], reverse=True)
        
        Results = "Leaderboard:\n"

        for x in sorted_wallets:
            Results += f"{guild.get_member(int(x[0])).name}: {x[1]}\n"
        await bot_channel.send(Results)
            