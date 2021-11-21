import discord
from discord.ext import commands
from decouple import config
from discord_gambler import _coinflip_channel, _guild_id
import datetime
import asyncio
import os
from discord_gambler.dao.user_wallets import UserWalletsDAO


class LeaderboardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leader", aliases=["leaderboard", "leaderboards", "lb"])
    async def on_leader_command(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            guild = discord.utils.get(self.bot.guilds, id=_guild_id)
            bot_channel = discord.utils.get(guild.text_channels, name=_coinflip_channel)
            top_wallets = UserWalletsDAO().get_top_wallets(_guild_id)

            embed = discord.Embed(
                title=f"Leaderboard",
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.blue(),
            )
            embed.set_author(name="Lagspike™")
            embed.set_footer(text=f"Made by Nrwls & Sparks")

            creators = ""
            coins = ""
            count = 1

            for x in top_wallets:
                user = guild.get_member(x[0])
                if user != None:
                    creators += f"{count}. {user.name}\n"
                    coins += f"{x[1]}\n"
                    count += 1

            embed.add_field(name="**__User__**", value=creators, inline=True)
            embed.add_field(name="**__Coins__**", value=coins, inline=True)
            await bot_channel.send(embed=embed, delete_after=10)
