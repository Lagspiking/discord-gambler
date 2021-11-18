from discord.ext import commands
from decouple import config
import logging
from discord_gambler import _coinflip_channel, _guild_id
import os

# https://discordpy.readthedocs.io/en/stable/api.html#event-reference
class MessageListeners(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        logging.info(
            f"Guild/Channel {message.channel.guild.id}/{message.channel.id}: {message.content}"
        )
        if (
            message.channel.name == _coinflip_channel
            and message.channel.guild.id == _guild_id
        ):
            if message.author != self._bot.user:
                if not message.content.startswith("!"):
                    try:
                        await message.message.delete()
                    except:
                        pass

    # An event that is called when a command is found and is about to be invoked.
    # This event is called regardless of whether the command itself succeeds via error or completes.
    @commands.Cog.listener()
    async def on_command(self, ctx):
        pass

    # An event that is called when a command has completed its invocation.
    # This event is called only if the command succeeded, i.e. all checks have passed and the user input it correctly.
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.channel.guild.id == _guild_id:
            try:
                await ctx.message.delete()
            except:
                pass

    # An error handler that is called when an error is raised inside a command either through user input error, check failure, or an error in your own code.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.channel.name == _coinflip_channel and ctx.channel.guild.id == _guild_id:
            await ctx.send(f"{error}")
            try:
                await ctx.message.delete()
            except:
                pass
