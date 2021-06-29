import discord
from discord.ext import commands
import random

class Coinflip(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot
        self.__coinflips = []

    async def create_coinflip(self, member, coins):
        self.__coinflips.append(CoinflipGame(member, coins))
        print(f"{member.id} has created a coinflip with value of {coins}")

    async def join_coinflip(self, creator, joiner):
        game = None
        for g in self.__coinflips:
            if await g.get_creator() == creator and await g.is_joinable():
                game = g

        await game.join(joiner)
        await game.flip()
        print(f"{await game.get_winner()} has won!")
        

    async def remove_coinfip(self, member):
        #remove a coinflip
        ...

    async def get_coinflips(self):
        return self.__coinflips

class CoinflipGame():
    def __init__(self, creator, coins):
        self.__creator = creator
        self.__coins = coins
        self.__joiner = None
        self.__winner = None

    async def flip(self):
        coinflip = random.randint(0, 1)

        if coinflip == 0:
            self.__winner = self.__creator
        else:
            self.__winner = self.__joiner

    async def join(self, member):
        self.__joiner = member

    async def is_joinable(self):
        return self.__joiner is None

    async def get_creator(self):
        return self.__creator

    async def get_winner(self):
        return self.__winner
