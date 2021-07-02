import discord
from discord.ext import commands, tasks
from decouple import config
from datetime import datetime
import random

class CoinsTasks(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._economy = self._bot.get_cog("Economy")
        self._coinflip_cog = self._bot.get_cog("Coinflip")
        self._voice = {}
        self.coins_reward_task.start()
        self.giveaway_jackpot.start()

    def cog_unload(self):
        self.coins_reward_task.cancel()
        self.giveaway_jackpot.cancel()

    @tasks.loop(seconds=10)
    async def coins_reward_task(self):
        if len(self._voice) == 0:
            self.get_users_in_voice_channels()

        for memberid in self._voice:
            member = await self._bot.get_guild(417762950200295444).fetch_member(memberid)
            self._economy.deposit(member, 50)

    @tasks.loop(seconds=30)
    async def giveaway_jackpot(self):
        if self._economy._jackpot >= 50000:
            #This is pretty cool, didn't know it existed lmao
            winner = random.choice(self._economy._jackpot_eligable)
            
            self._economy.deposit(winner, self._economy._jackpot)
            #When sending a chat message, prefix the sentence with > for cooler looking markup.
            await self._bot.get_channel(859490586976845844).send(f"> {winner.mention} has won the jackpot of {self._economy._jackpot}", delete_after=5)
            #_variables are prefixed with _ because they're meant to be private. If you want to access/modify it, you should create a getter/setter x
            self._economy._jackpot = 0

    @coins_reward_task.before_loop
    async def before_coins_reward_task(self):
        await self._bot.wait_until_ready()

    @giveaway_jackpot.before_loop
    async def before_giveaway_jackpot(self):
        await self._bot.wait_until_ready()

    def get_users_in_voice_channels(self):
        for channel in self._bot.get_guild(417762950200295444).channels:
            if channel.type == discord.ChannelType.voice and len(channel.members) > 0:
                for member in channel.members:
                    self._voice[str(member.id)] = datetime.now()