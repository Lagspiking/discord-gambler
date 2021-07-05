import discord
import discord.utils
from discord.ext import commands, tasks
from decouple import config
from datetime import datetime
import random

class VoiceChannelTasks(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._players_cog = self._bot.get_cog("Players")
        self.active_voice_channel_members_task.start()

    def cog_unload(self):
        self.active_voice_channel_members_task.cancel()

    @tasks.loop(seconds=10)
    async def active_voice_channel_members_task(self):
        for channel in self._bot.get_guild(417762950200295444).channels:
            if channel.type == discord.ChannelType.voice and len(channel.members) > 0:
                for member in channel.members:
                    if self._players_cog.get_player(member) is not None:
                        self._players_cog.get_player(member).last_active = datetime.now
                        self._players_cog.get_player(member).last_updated = datetime.now
                    else:
                        self._players_cog.add_player(member)
    
    @active_voice_channel_members_task.before_loop
    async def before_active_voice_channel_members_task(self):
        await self._bot.wait_until_ready()
