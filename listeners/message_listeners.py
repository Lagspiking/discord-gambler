from discord.ext import commands
from decouple import config

#https://discordpy.readthedocs.io/en/stable/api.html#event-reference
class MessageListeners(commands.Cog):
    
    def __init__(self, bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name == config('channel_name'):
            if message.author != self._bot.user:
                if not message.content.startswith("!"):
                    await message.delete()

    #An event that is called when a command is found and is about to be invoked.
    #This event is called regardless of whether the command itself succeeds via error or completes.
    @commands.Cog.listener()
    async def on_command(self, ctx):
        pass

    #An event that is called when a command has completed its invocation.
    #This event is called only if the command succeeded, i.e. all checks have passed and the user input it correctly.
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await ctx.message.delete()

    #An error handler that is called when an error is raised inside a command either through user input error, check failure, or an error in your own code.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.message.delete()