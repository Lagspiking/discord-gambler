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

    def get_open_coinflips_message(self):
        print("get_open_coinflips")
        embed = discord.Embed(title=f"Coinflips", color=discord.Color.red())
        embed.set_author(name="Lagspike™")
        embed.set_footer(text=f"Made by Nrwls & Sparks")

        if len(self.get_coinflips()) == 0:
            embed.add_field(name="**No games to show**", value="Type !c [coins] to create a coinflip.", inline=True)
            return embed

        creators = ""
        prices = ""

        for coinflip in self.get_coinflips():
            if coinflip.is_joinable():
                print("iterated open")
                if coinflip.get_creator() is not None and coinflip.get_coins() is not None:
                    creators += f"{coinflip.get_creator().mention}\n"
                    prices += f"{coinflip.get_coins()} coins\n"

        print(creators)
        print(prices)

        embed.add_field(name="**__User__**", value=creators, inline=True)
        embed.add_field(name="**__Stake__**", value=prices, inline=True)
        return embed

    def get_coinflip_results_message(self):
        print("get_coinflips_results")
        embed = discord.Embed(title=f"Coinflip Results", color=discord.Color.red())
        embed.set_author(name="Lagspike™")
        embed.set_footer(text=f"Made by Nrwls & Sparks")

        #cf = [x for x in self.get_coinflips() if x.is_finished()]
        print(self.get_coinflips())

        if len(self.get_coinflips()) == 0:
            embed.add_field(name="**No results to show**", value="Type !c [coins] to create a coinflip.", inline=True)
            return embed
        
        winners = ""
        prices = ""
        losers = ""

        for coinflip in self.get_coinflips():
            if not coinflip.is_joinable():
                print("iterated results")
                winners += f"{coinflip.get_winner().mention}\n"
                prices += f"{coinflip.get_coins()} coins\n"
                losers += f"{coinflip.get_loser().mention}\n"

        embed.add_field(name="**__Winner__**", value=winners, inline=True)
        embed.add_field(name="**Stake**", value=prices, inline=True)
        embed.add_field(name="**__Loser__**", value=losers, inline=True)
        return embed