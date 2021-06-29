import discord
from discord.ext import commands

class Coinflip(commands.Cog):

    def __init__(self):
        self.coinflips = {}

    async def create_coinflip(self, member, coins):
        print(f"{member.id} has created a coinflip with value of {coins}")
        #self.coinflips.add()

    async def join_conflip(self, member):
        #join a coinflip
        ...

    async def remove_coinfip(self, member):
        #remove a coinflip
        ...