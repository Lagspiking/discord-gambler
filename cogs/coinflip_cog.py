from discord.ext import commands
from games.coinflip_game import CoinflipGame

class CoinflipCog(commands.Cog, name = "Coinflip"):

    def __init__(self, bot):
        self._bot = bot
        self._coinflips = []

    def create_coinflip(self, member, coins):
        self._coinflips.append(CoinflipGame(member, coins))

    def join_coinflip(self, creator, joiner):
        game = self.get_coinflip_game(creator)
        game.join(joiner)

    def run_coinflip(self, creator):
        game = self.get_coinflip_game(creator)
        game.flip()

    def get_coinflip_game(self, creator):
        game = None
        for g in self._coinflips:
            if g.get_creator() == creator:
                game = g
        return game

    def remove_coinflip(self, member):
        game = self.get_coinflip_game(member)
        self._coinflips.remove(game)

    def get_coinflips(self):
        return self._coinflips