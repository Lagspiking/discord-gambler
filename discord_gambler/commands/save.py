from discord.ext import commands
from discord_gambler import _coinflip_channel, _guild_id
import json


class SaveCommand(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._economy_cog = self._bot.get_cog("Economy")
        self._coinflip_cog = self._bot.get_cog("Coinflip")
        self._save_state = {}
        self.load_data(self)

    @staticmethod
    def save_data(self):
        self._save_state["wallets"] = self._economy_cog.get_all_wallets()
        self._save_state["current_jackpot"] = self._coinflip_cog.get_giveaway()

        # TODO: Handle saving and loading within a cog
        with open("save.json", "w") as outfile:
            json.dump(self._save_state, outfile, sort_keys=True, indent=4)

    @commands.command(name="save", aliases=["s"])
    async def on_save_command(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            self.save_data(self)

    @staticmethod
    def load_data(self):
        with open("save.json") as outfile:
            data = json.load(outfile)
            self._economy_cog.set_all_wallets(data["wallets"])
            self._coinflip_cog.set_giveaway(data["current_jackpot"])

    @commands.command(name="load", aliases=["l"])
    async def on_load_command(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            self.load_data(self)
