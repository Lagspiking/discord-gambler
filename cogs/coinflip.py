import discord
from discord.ext import commands
import random

class Coinflip(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot
        self.__coinflips = []

    async def create_coinflip(self, ctx, member, coins):
        self.__coinflips.append(CoinflipGame(member, coins))
        await ctx.send(f"{member.id} has created a coinflip with value of {coins}")

    async def join_coinflip(self, ctx, creator, joiner):
        game = None
        for g in self.__coinflips:
            if await g.get_creator() == creator and await g.is_joinable():
                game = g

        await game.join(joiner)
        await game.flip()
        await ctx.send(f"{await game.get_winner()} has won {await game.get_coins() * 2} against {await game.get_loser()}!")
        
    async def get_coinflip_game(self, creator):
        game = None
        for g in self.__coinflips:
            if await g.get_creator() == creator and await g.is_joinable():
                game = g
        return game

    async def remove_coinfip(self, member):
        #remove a coinflip
        ...

    async def get_coinflips(self):
        return self.__coinflips

class CoinflipGame():
    def __init__(self, creator, coins):
        self.__creator = creator
        self.__joiner = None
        self.__coins = coins
        self.__winner = None
        self.__loser = None

    async def flip(self):
        coinflip = random.randint(0, 1)

        if coinflip == 0:
            self.__winner = self.__creator
            self.__loser = self.__joiner
        else:
            self.__winner = self.__joiner
            self.__loser = self.__creator

    async def join(self, member):
        self.__joiner = member

    async def is_joinable(self):
        return self.__joiner is None

    async def get_creator(self):
        return self.__creator

    async def get_winner(self):
        return self.__winner
    
    async def get_loser(self):
        return self.__loser

    async def get_coins(self):
        return self.__coins
