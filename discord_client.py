from cogs import *
import discord
import logging
from discord.ext import commands
from decouple import config

logging.basicConfig(level=logging.INFO)

#setup Discord
_token = config("discord_token")
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

#register our models
bot.add_cog(Economy(bot))
bot.add_cog(Coinflip(bot))

#register our commands/cogs
bot.add_cog(CurrencyCommand(bot))
bot.add_cog(LeaderboardsCommand(bot))
bot.add_cog(TestCommand(bot))

bot.run(_token)