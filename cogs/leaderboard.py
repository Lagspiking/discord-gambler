import discord
from discord.ext import commands

class LeaderboardsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "leaderboards")
    async def on_leaderboards_command(self, ctx):
        print("leaderboards")