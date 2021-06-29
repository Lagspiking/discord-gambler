import discord
from discord.ext import commands

class Economy(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot
        self.__wallets = {}

    async def withdraw_coins(self, member, money):
        print(f"withdrawing {money} from {member}")

    async def deposit_coins(self, member, money):
        print(f"depositing {money} to {member}")

    async def get_wallet(self, member):
        exists = await self.wallet_exists(member)
        if not exists:
            await self.create_wallet(member)

        return self.__wallets.get(member.id)

    async def wallet_exists(self, member):
        return self.__wallets[member.id] is not None

    async def create_wallet(self, member):
        self.__wallets[member.id] = 0