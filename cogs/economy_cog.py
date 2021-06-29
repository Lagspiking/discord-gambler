import discord
from discord.ext import commands

class EconomyCog(commands.Cog, name = "Economy"):

    def __init__(self, bot):
        self._bot = bot
        self._wallets = {}
        self._default_coins = 1000

    #Checks if a member has a specific amount of coins in their wallet.
    def has_coins(self, member, coins):
        wallet = self.get_wallet(member)
        return wallet > 0 and wallet >= coins

    #Get a wallet of a member
    def get_wallet(self, member):
        if not self.wallet_exists(member):
            self.create_wallet(member)
        return self._wallets.get(str(member.id))

    #Check if a members wallet exists, if not, create one.
    def wallet_exists(self, member):
        return str(member.id) in self._wallets
    
    #Creates a new wallet for a member with a default set of coins.
    def create_wallet(self, member):
        self._wallets[str(member.id)] = self._default_coins

    #Updates a members wallet with a n amount of coins.
    def update_wallet(self, member, coins):
        self._wallets[str(member.id)] = coins

    #Withdraws coins from a member. Normally used in conjunction with deposit_coins.
    def withdraw(self, member, coins):
        wallet = self.get_wallet(member)
        self.update_wallet(member, wallet - coins)

    #Deposit coins to a member. Normally used in conjuction with withdraw_coins.
    def deposit(self, member, coins):
        wallet = self.get_wallet(member)
        self.update_wallet(member, wallet + coins)