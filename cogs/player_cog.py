import discord
import datetime
from discord.ext import commands
from games.coinflip_game import CoinflipGame

class PlayerCog(commands.Cog, name = "Player"):
    def __init__(self, bot):
        self._bot = bot
        self._players = {}
    
    def load_players(self):
        #Load players from a json file locally or something
        #so that we can maintain their wallet state or coinflips
        pass

    def add_player(self, member: discord.Member):
        self._players[str(member.id)] = Player(member)

    def remove_player(self, member: discord.Member):
        self._players.pop(str(member.id))

    def get_player(self, member:discord.Member):
        return self._players[str(member.id)]

class Player():
    def __init__(self, member: discord.Member):
        self._member = member
        self._wallet = Wallet(1000)

    def get_member(self):
        return self._member

    def get_wallet(self):
        return self._wallet

    member = property(get_member)
    wallet = property(get_wallet)

class Wallet():
    def __init__(self, coins: int):
        self._coins = coins

    def get_wallet(self):
        return self._coins

    def set_wallet(self, coins: int):
        self._coins = coins

    coins = property(get_wallet, set_wallet)