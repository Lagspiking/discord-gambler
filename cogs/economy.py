import discord
from discord.ext import commands

class Economy(commands.Cog):

    async def withdraw_coins(self, member, money):
        print(f"withdrawing {money} from {member}")

    async def deposit_coins(self, member, money):
        print(f"depositing {money} to {member}")

    async def get_coins(self, member):
        print(0)