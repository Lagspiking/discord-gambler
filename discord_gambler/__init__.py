import discord
import logging
from discord.ext import commands
from decouple import config
import os

# setup Discord
try:
    _token = config("discord_token")
    _coinflip_channel = config("coinflip_channel_name")
    _guild_id = int(config("guild_id"))
except:
    _token = os.environ.get("discord_token")
    _coinflip_channel = os.environ.get("coinflip_channel_name")
    _guild_id = os.environ.get("guild_id")

from discord_gambler.listeners import *
from discord_gambler.cogs import *
from discord_gambler.commands import *
from discord_gambler.tasks import *

logging.basicConfig(level=logging.INFO)


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# register our listeners
bot.add_cog(DiscordListeners(bot))
bot.add_cog(MessageListeners(bot))
bot.add_cog(MemberListeners(bot))
# bot.add_cog(VoiceListeners(bot))
bot.add_cog(GuildListeners(bot))

# register our logic cogs
# bot.add_cog(DatabaseCog(bot))
bot.add_cog(EconomyCog(bot))
bot.add_cog(CoinflipCog(bot))

# register our commands
bot.add_cog(CoinsCommand(bot))
bot.add_cog(CleanseCommand(bot))
bot.add_cog(LeaderboardCommand(bot))
bot.add_cog(CoinflipCommand(bot))
bot.add_cog(SaveCommand(bot))
bot.add_cog(SoundsCommand(bot))

# register our background tasks
bot.add_cog(CoinsTasks(bot))
