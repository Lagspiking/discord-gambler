import discord
import datetime
from discord.ext import commands
from discord_gambler.games.coinflip_game import CoinflipGame


class PlayersCog(commands.Cog, name="Players"):
    def __init__(self, bot):
        self._bot = bot
        self._players = {}

    def load_players(self):
        # Load players from a json file locally or something
        # so that we can maintain their wallet state or coinflips
        pass

    def add_player(self, member: discord.Member):
        self._players[str(member.id)] = Player(member)

    def remove_player(self, member: discord.Member):
        self._players.pop(str(member.id))

    def get_player(self, member: discord.Member):
        return self._players[str(member.id)]

    def get_players(self):
        return self._players


class Player:
    def __init__(self, member: discord.Member):
        self._member = member
        self._wallet = Wallet(1000)
        self._last_active = datetime.datetime.now
        self._last_updated = datetime.datetime.now

    def get_member(self):
        return self._member

    def get_wallet(self):
        return self._wallet

    def get_last_active(self):
        return self._last_active

    def set_last_active(self, datetime: datetime.datetime):
        self._last_active = datetime

    def get_last_updated(self):
        return self._last_updated

    def set_last_updated(self, datetime: datetime.datetime):
        self._last_updated = datetime

    member = property(get_member)
    wallet = property(get_wallet)
    last_active = property(get_last_active, set_last_active)
    last_updated = property(get_last_updated, set_last_updated)


class Wallet:
    def __init__(self, coins: int):
        self._coins = coins

    def get_coins(self):
        return self._coins

    def set_coins(self, coins: int):
        self._coins = coins

    coins = property(get_coins, set_coins)
