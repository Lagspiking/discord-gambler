import discord
from discord.ext import commands

class Economy(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot
        self.__wallets = {}

    async def withdraw_coins(self, ctx, member, coins):
        wallet = await self.get_wallet(member)

        if wallet > coins:
            print(f"Not enough money in wallet!")

        await self.update_wallet(member, wallet - coins)

        print(f"Withdrawing {coins} from {member}")

    async def deposit_coins(self, ctx, member, money):
        print(f"depositing {money} to {member}")

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