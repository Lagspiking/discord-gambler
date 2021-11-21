import discord
from discord.ext import commands
from discord_gambler.games.coinflip_game import CoinflipGame
from ..dao.user_wallets import UserWalletsDAO
from ..dao.coinflips import CoinflipsDAO
import random
from discord_gambler import _guild_id


class CoinflipCog(commands.Cog, name="Coinflip"):
    def __init__(self, bot):
        self._bot = bot
        self._economy_cog = self._bot.get_cog("Economy")
        self._coinflips = []
        self._giveaway = 0
        self._giveaway_eligable = []
        self._giveaway_members = {}

    def create_coinflip(self, member: discord.Member, coins: int):
        self._economy_cog.withdraw(member, coins)
        self._coinflips.append(CoinflipGame(member, coins))

    def join_coinflip(self, creator: discord.Member, joiner: discord.Member):
        game = self.get_coinflip_game(creator)
        self._economy_cog.withdraw(joiner, game.get_coins())
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
        self._economy_cog.deposit(game.get_winner(), int(game.get_coins() * 1.8))

        # Tax the house takes to populate the giveaway
        self._giveaway += int(game.get_coins() * self._giveaway_tax)

    def run_giveaway(self):
        """Returns back a tuple containing the user object and win percentage"""
        print(self._giveaway_members)
        percentages = {}
        for member in self._giveaway_members:
            # Assume 2 users coinflip 1,000,000 and the giveaway will only contain the taxed coins from that coinflip
            # We tax 20% of the total coins, meaning we actually tax 10% from each user (100,000 from each user, 200,000 tax total)
            # So the calculation is:
            # (1,000,000 * 0.2) = 200,000 -> Tax Total
            # (200,000 / 2) = 100,000     -> Tax from each person
            # (100,000 / 200,000) = 0.5   -> Win percentage as decimal
            # (0.5 * 100) = 50            -> Win percentage
            taxTotal = int(self._giveaway_members[member] * self._giveaway_tax)
            taxPerPerson = int(taxTotal / 2)
            winPercentage = (taxPerPerson / self._giveaway) * 100
            percentages[member.id] = int(winPercentage)
        print(percentages)

        picks = [
            v
            for v, d in zip(percentages.keys(), percentages.values())
            for x in range(d)
        ]
        winner = self._bot.get_guild(_guild_id).get_member(random.choice(picks))

        self._economy_cog.deposit(winner, self._giveaway)

        result = winner, percentages[winner.id], self._giveaway

        self._giveaway = 0
        self._giveaway_eligable = []
        self._giveaway_members = {}
        return result

    def get_coinflip_game(self, creator: discord.Member):
        game = None
        for g in self._coinflips:
            if g.get_creator() == creator:
                game = g
        return game

    def get_open_coinflip_game(self, creator: discord.Member):
        game = None
        for g in self._coinflips:
            if g.get_creator() == creator and g.is_joinable():
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
        game = self.get_open_coinflip_game(member)
        self._economy_cog.deposit(member, game.get_coins())
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

        guild = discord.utils.get(self._bot.guilds, id=_guild_id)
        creators = ""
        prices = ""
        for coinflip in CoinflipsDAO().get_open_coinflips().items():
            user = guild.get_member(coinflip[0])
            if user != None:
                creators += f"{guild.get_member(int(coinflip[0])).mention}\n"
                prices += f"{coinflip[1]} coins\n"

        if creators != "":
            embed.add_field(name="**User**", value=creators, inline=True)
            embed.add_field(name="**Stake**", value=prices, inline=True)

            embed.add_field(
                name="**Commands**",
                value="\n Type _!coins_ to check your wallet.\n Type _!c [coins]_ to create a coinflip.\n Type _!j [@mention]_ to join a coinflip.\n Type _!leader_ to see the leaderboards.\n Type _!give [@mention] [coins]_ to give someone coins.\n Type _!wl_ to see your win/loss.",
                inline=False,
            )
        else:
            embed.add_field(name="_No active coinflips_", value="\u200b", inline=True)
        return embed

    def get_coinflip_results_message(self):
        embed = discord.Embed(
            title=f"__Previous Coinflips__", color=discord.Color.blue()
        )
        embed.set_author(name=f"Lagspike™")

        guild = discord.utils.get(self._bot.guilds, id=_guild_id)

        winners = ""
        prices = ""
        losers = ""

        for coinflip in CoinflipsDAO().get_recent_coinflips():
            user = guild.get_member(coinflip[0])
            if user != None:
                winners += f"{guild.get_member(int(coinflip[0])).mention}\n"
                prices += f"{coinflip[1]} coins\n"
                losers += f"{guild.get_member(int(coinflip[2])).mention}\n"

        if winners != "":
            embed.add_field(name="**__Winner__**", value=winners, inline=True)
            embed.add_field(name="**Stake**", value=prices, inline=True)
            embed.add_field(name="**__Loser__**", value=losers, inline=True)
        else:
            embed.add_field(name="_No previous coinflips_", value="\u200b", inline=True)
            return embed
        return embed
