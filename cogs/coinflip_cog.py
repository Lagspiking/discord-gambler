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

    def get_coinflip_message(self):
        embed = discord.Embed(title=f"Coinflips", color=discord.Color.red())
        embed.set_author(name="Lagspike™")
        embed.set_footer(text=f"Made by Nrwls & Sparks")

        creators = ""
        prices = ""
        joiners = ""

        for coinflip in self.get_coinflips():
            if coinflip.is_joinable():
                creators += f"{coinflip.get_creator().mention}\n"
                prices += f"{coinflip.get_coins()} coins\n"
                #joiners += "Joinable\n"

        embed.add_field(name="**__User__**", value=creators, inline=True)
        embed.add_field(name="**Stake**", value=prices, inline=True)
        #embed.add_field(name="**__User__**", value=joiners, inline=True)
        return embed

    def get_coinflip_setup_message(self):
        embed = discord.Embed(title=f"Coinflips", color=discord.Color.red())
        embed.set_author(name="Lagspike™")
        embed.set_footer(text=f"Made by Nrwls & Sparks")
        embed.add_field(name="**No games to show**", value="Type !c [coins] to create a coinflip.", inline=True)
        return embed