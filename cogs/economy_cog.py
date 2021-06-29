import discord
from discord.ext import commands

class EconomyCog(commands.Cog, name = "Economy"):

    def __init__(self, bot):
        self.__bot = bot
        self.__wallets = {}

    async def withdraw_coins(self, member, coins):
        wallet = await self.get_wallet(member)
        await self.update_wallet(member, wallet - coins)

    async def deposit_coins(self, member, coins):
        wallet = await self.get_wallet(member)
        await self.update_wallet(member, wallet + coins)

    async def get_wallet(self, member):
        exists = await self.wallet_exists(member)
        if not exists:
            await self.create_wallet(member)

        return self.__wallets.get(str(member.id))

    async def wallet_exists(self, member):
        return str(member.id) in self.__wallets

    async def create_wallet(self, member):
        self.__wallets[str(member.id)] = 1000

    async def update_wallet(self, member, coins):
        self.__wallets[str(member.id)] = coins