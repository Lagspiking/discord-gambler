import discord
import datetime
from discord.ext import commands
from games.coinflip_game import CoinflipGame

class CoinflipCog(commands.Cog, name = "Coinflip"):

    def __init__(self, bot):
        self._bot = bot
        self._coinflips = []

    def create_coinflip(self, member: discord.Member, coins: int):
        self._coinflips.append(CoinflipGame(member, coins))

    def join_coinflip(self, creator: discord.Member, joiner: discord.Member):
        game = self.get_coinflip_game(creator)
        game.join(joiner)

    def run_coinflip(self, creator: discord.Member):
        game = self.get_coinflip_game(creator)
        game.flip()

    def get_coinflip_game(self, creator: discord.Member):
        game = None
        for g in self._coinflips:
            if g.get_creator() == creator:
                game = g
        return game

    def remove_coinflip(self, member: discord.Member):
        game = self.get_coinflip_game(member)
        self._coinflips.remove(game)

    def get_coinflips(self):
        return self._coinflips

    def get_most_recent_coinflip_results(self):
        results = [x for x in self.get_coinflips() if not x.is_joinable()]
        return results[-10:]

    def get_open_coinflips_message(self):
        embed = discord.Embed(title=f"__Joinable Coinflips__", color=discord.Color.red())
        embed.set_author(name="Lagspike™")
        embed.set_footer(text=f"Made by Nrwls & Sparks")

        if len(self.get_coinflips()) == 0 or len([x for x in self.get_coinflips() if x.is_joinable()]) == 0:
            embed.add_field(name="**No active coinflips**", value="\u200b", inline=True)
        else:
            creators = ""
            prices = ""

            for coinflip in self.get_coinflips():
                if coinflip.is_joinable():
                    if coinflip.get_creator() is not None and coinflip.get_coins() is not None:
                        creators += f"{coinflip.get_creator().mention}\n"
                        prices += f"{coinflip.get_coins()} coins\n"

            embed.add_field(name="**User**", value=creators, inline=True)
            embed.add_field(name="**Stake**", value=prices, inline=True)

        embed.add_field(name="**Commands**", value="Type _!c [coins]_ to create a coinflip.\n Type _!j [@mention]_ to join a coinflip.\n Type _!coins_ to check your wallet.\n Type _!leader_ to see the leaderboards.\n Type _!give [@mention] [coins]_ to give someone coins.", inline=False)

        return embed

    def get_coinflip_results_message(self):
        embed = discord.Embed(title=f"__Previous Coinflips__", color=discord.Color.red())
        embed.set_author(name="Lagspike™")
        embed.set_footer(text=f"Made by Nrwls & Sparks")

        if len(self.get_coinflips()) == 0 or len([x for x in self.get_coinflips() if not x.is_joinable()]) == 0:
            embed.add_field(name="**No previous coinflips to show**", value="\u200b", inline=True)
            return embed
        
        winners = ""
        prices = ""
        losers = ""

        for coinflip in self.get_most_recent_coinflip_results():
            winners += f"{coinflip.get_winner().mention}\n"
            prices += f"{coinflip.get_coins()} coins\n"
            losers += f"{coinflip.get_loser().mention}\n"

        embed.add_field(name="**__Winner__**", value=winners, inline=True)
        embed.add_field(name="**Stake**", value=prices, inline=True)
        embed.add_field(name="**__Loser__**", value=losers, inline=True)
        return embed