import discord
from discord.ext import commands, tasks

class CoinsTasks(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._economy = self._bot.get_cog("Economy")
        self.coins_reward_task.start()

    def cog_unload(self):
        self.coins_reward_task.cancel()

    @tasks.loop(minutes=1)
    async def coins_reward_task(self):
        pass

    @coins_reward_task.before_loop
    async def before_coins_reward_task(self):
        await self._bot.wait_until_ready()