from cogs import *
from commands import *
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
bot.add_cog(EconomyCog(bot))
bot.add_cog(CoinflipCog(bot))

#register our commands/cogs
bot.add_cog(CoinsCommand(bot))
bot.add_cog(CoinflipCommand(bot))

bot.run(_token)