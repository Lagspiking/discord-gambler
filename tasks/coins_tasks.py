import discord
from discord.ext import commands, tasks
from decouple import config
from datetime import datetime

class CoinsTasks(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._economy = self._bot.get_cog("Economy")
        self._voice = {}
        self.coins_reward_task.start()

    def cog_unload(self):
        self.coins_reward_task.cancel()

    @tasks.loop(seconds=10)
    async def coins_reward_task(self):
        if len(self._voice) == 0:
            self.get_users_in_voice_channels()

        for memberid in self._voice:
            member = await self._bot.get_guild(417762950200295444).fetch_member(memberid)
            self._economy.deposit(member, 1000)

    @coins_reward_task.before_loop
    async def before_coins_reward_task(self):
        await self._bot.wait_until_ready()

    def get_users_in_voice_channels(self):
        for channel in self._bot.get_guild(417762950200295444).channels:
            if channel.type == discord.ChannelType.voice and len(channel.members) > 0:
                for member in channel.members:
                    self._voice[str(member.id)] = datetime.now()

