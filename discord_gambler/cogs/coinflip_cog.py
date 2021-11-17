import discord
from discord.ext import commands
from discord_gambler.games.coinflip_game import CoinflipGame
import random


class CoinflipCog(commands.Cog, name="Coinflip"):
    def __init__(self, bot):
        self._bot = bot
        self._economy = self._bot.get_cog("Economy")
        self._coinflips = []
        self._giveaway = 0
        self._giveaway_eligable = []
        self._giveaway_members = {}

    def create_coinflip(self, member: discord.Member, coins: int):
        self.economy_cog.withdraw(member, coins)
        self._coinflips.append(CoinflipGame(member, coins))

    def join_coinflip(self, creator: discord.Member, joiner: discord.Member):
        game = self.get_coinflip_game(creator)
        self.economy_cog.withdraw(joiner, game.get_coins())
        game.join(joiner)

    def run_coinflip(self, creator: discord.Member):
        game = self.get_coinflip_game(creator)
        game.flip()
        
        if game.get_winner() not in self._giveaway_members:
            self._giveaway_members[game.get_winner()] = game.get_coins()
        else:
            self._giveaway_members[game.get_winner()] += game.get_coins()

        if game.get_loser() not in self._giveaway_members:
            self._giveaway_members[game.get_loser()] = game.get_coins()
        else:
            self._giveaway_members[game.get_loser()] += game.get_coins()

        # Give the winner the coins minus the giveaway tax
        self.economy_cog.deposit(
            game.get_winner(), int(game.get_coins() * 1.8)
        )

        # Tax the house takes to populate the giveaway
        self.coinflip_cog._giveaway += int(game.get_coins() * 0.2)

    def run_giveaway(self):
        '''Returns back a tuple containing the user object and win percentage'''
        percentages = {}
        for member in self._giveaway_members:
            percentages[member] = (
                self._giveaway_members[member] / self._giveaway
            ) * 100

        picks = [v for v, d in zip(percentages.keys(), percentages.values()) for x in range(d)]
        winner = random.choice(picks)

        self._economy.deposit(winner, self._coinflip_cog._giveaway)

        self._coinflip_cog._giveaway = 0
        self._coinflip_cog._giveaway_eligable = []
        self._coinflip_cog._giveaway_members = {}
        return winner, percentages[winner]

    def get_coinflip_game(self, creator: discord.Member):
        game = None
        for g in self._coinflips:
            if g.get_creator() == creator:
                game = g
        return game

    def get_giveaway(self):
        return self._giveaway

    def set_giveaway(self, giveaway):
        self._giveaway = giveaway

    def get_giveaway_eligable(self):
        return self._giveaway_eligable

    def set_giveaway_eligable(self, eligable):
        self._giveaway_eligable = eligable

    def remove_coinflip(self, member: discord.Member):
        game = self.get_coinflip_game(member)
        self.economy_cog.deposit(member, game.get_coins())
        self._coinflips.remove(game)

    def get_coinflips(self):
        return self._coinflips

    def get_most_recent_coinflip_results(self):
        results = [x for x in self.get_coinflips() if not x.is_joinable()]
        return results[-10:]

    def get_open_coinflips_message(self):
        embed = discord.Embed(
            title=f"__Joinable Coinflips__", color=discord.Color.blue()
        )
        embed.set_author(name=f"Lagspike™ | Giveaway: {self._giveaway}")
        embed.set_footer(text=f"Made by Nrwls & Sparks")

        if (
            len(self.get_coinflips()) == 0
            or len([x for x in self.get_coinflips() if x.is_joinable()]) == 0
        ):
            embed.add_field(name="_No active coinflips_", value="\u200b", inline=True)
        else:
            creators = ""
            prices = ""

            for coinflip in self.get_coinflips():
                if coinflip.is_joinable():
                    if (
                        coinflip.get_creator() is not None
                        and coinflip.get_coins() is not None
                    ):
                        creators += f"{coinflip.get_creator().mention}\n"
                        prices += f"{coinflip.get_coins()} coins\n"

            embed.add_field(name="**User**", value=creators, inline=True)
            embed.add_field(name="**Stake**", value=prices, inline=True)

        embed.add_field(
            name="**Commands**",
            value="\n Type _!coins_ to check your wallet.\n Type _!c [coins]_ to create a coinflip.\n Type _!j [@mention]_ to join a coinflip.\n Type _!leader_ to see the leaderboards.\n Type _!give [@mention] [coins]_ to give someone coins.\n Type _!wl_ to see your win/loss.",
            inline=False,
        )

        return embed

    def get_coinflip_results_message(self):
        embed = discord.Embed(
            title=f"__Previous Coinflips__", color=discord.Color.blue()
        )
        embed.set_author(name=f"Lagspike™")

        if (
            len(self.get_coinflips()) == 0
            or len([x for x in self.get_coinflips() if not x.is_joinable()]) == 0
        ):
            embed.add_field(
                name="_No previous coinflips_", value="\u200b", inline=True
            )
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
