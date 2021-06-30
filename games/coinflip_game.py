import random
import discord

class CoinflipGame():
    def __init__(self, creator: discord.Member, coins: int):
        self._creator = creator
        self._joiner = None
        self._coins = coins
        self._winner = None
        self._loser = None

    def flip(self):
        coinflip = random.randint(0, 1)

        if coinflip == 0:
            self._winner = self._creator
            self._loser = self._joiner
        else:
            self._winner = self._joiner
            self._loser = self._creator

    def join(self, member):
        self._joiner = member

    def is_joinable(self):
        return self._joiner is None

    def get_creator(self):
        return self._creator

    def get_winner(self):
        return self._winner
    
    def get_loser(self):
        return self._loser

    def get_coins(self):
        return self._coins