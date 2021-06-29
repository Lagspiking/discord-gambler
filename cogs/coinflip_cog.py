from discord.ext import commands
from games.coinflip_game import CoinflipGame

class CoinflipCog(commands.Cog, name = "Coinflip"):

    def __init__(self, bot):
        self.__bot = bot
        self.__coinflips = []

    async def create_coinflip(self, member, coins):
        self.__coinflips.append(CoinflipGame(member, coins))

    async def join_coinflip(self, creator, joiner):
        game = await self.get_coinflip_game(creator)
        await game.join(joiner)

    async def run_coinflip(self, creator):
        game = await self.get_coinflip_game(creator)
        await game.flip()

    async def get_coinflip_game(self, creator):
        game = None
        for g in self.__coinflips:
            if await g.get_creator() == creator:
                game = g
        return game

    async def remove_coinfip(self, member):
        #remove a coinflip
        ...

    async def get_coinflips(self):
        return self.__coinflips