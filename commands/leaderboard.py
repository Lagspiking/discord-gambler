import discord
from discord.ext import commands
from decouple import config
import datetime
import asyncio

class LeaderboardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="leader")
    async def on_leader_command(self, ctx):
        guild = discord.utils.get(self.bot.guilds, name="$ui$lide")
        bot_channel = discord.utils.get(guild.text_channels, name="gamble-bot")
        economy = self.bot.get_cog("Economy")
        all_wallets = economy.get_all_wallets()
        sorted_wallets = sorted(all_wallets.items(), key=lambda x: x[1], reverse=True)
        
        embed = discord.Embed(title=f"Leaderboard", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed.set_author(name="Lagspike™")
        embed.set_footer(text=f"Made by Nrwls & Sparks")

        creators = ""
        coins = ""
        count = 1

        for x in sorted_wallets:
            if count < 6:
                creators += f"{count}. {guild.get_member(int(x[0])).name}\n"
                coins += f"{x[1]}\n"
                count += 1
        
        embed.add_field(name="**__User__**", value=creators, inline=True)
        embed.add_field(name="**__Coins__**", value=coins, inline=True)
        await ctx.message.delete()
        await bot_channel.send(embed=embed, delete_after=10)