import random

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

    def join(self, member):
        self.__joiner = member

    def is_joinable(self):
        return self.__joiner is None

    def get_creator(self):
        return self.__creator

    def get_winner(self):
        return self.__winner
    
    def get_loser(self):
        return self.__loser

    def get_coins(self):
        return self.__coins