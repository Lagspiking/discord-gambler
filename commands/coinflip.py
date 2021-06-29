import discord
from discord.ext import commands
import typing

class CoinflipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "create")
    async def on_create_coinflip_command(self, ctx, coins: int):
        economy = self.bot.get_cog("Economy")
        coinflip = self.bot.get_cog("Coinflip")
        
        #Get the users wallet/coins
        userCoins = await economy.get_wallet(ctx.author)
        
        if coins <= 0:
            await ctx.send(f"You cannot create a zero/negative value coinflip.")
        elif userCoins < coins:
            await ctx.send(f"You do not have enough coins to create this coinflip.")
        elif userCoins >= coins:
            await economy.withdraw_coins(ctx.author, coins)
            await coinflip.create_coinflip(ctx.author, coins)
            await ctx.send(f"{ctx.author} has created a coinflip for {coins} coins!")

    @commands.command(name = "join")
    async def on_join_coinflip_command(self, ctx, member: discord.Member):
        economy = self.bot.get_cog("Economy")
        coinflip = self.bot.get_cog("Coinflip")

        game = await coinflip.get_coinflip_game(member)
        if game is None:
            await ctx.send(f"A game by that user does not exist.")
            return

        if not await game.is_joinable():
            await ctx.send(f"That game is not joinable.")
            return

        userCoins = await economy.get_wallet(ctx.author)
        if userCoins < await game.get_coins():
            await ctx.send(f"You do not have enough coins to join this coinflip.")
            return

        await economy.withdraw_coins(ctx.author, await game.get_coins())
        await coinflip.join_coinflip(member, ctx.author)
        await coinflip.run_coinflip(await game.get_creator())
        await economy.deposit_coins(await game.get_winner(), await game.get_coins() * 2)
        await ctx.send(f"{await game.get_winner()} has won {await game.get_coins()} coins from {await game.get_loser()}")

    @commands.command(name = "remove")
    async def on_remove_coinflip_command(self, ctx):
        economy = self.bot.get_cog("Economy")
        coinflip = self.bot.get_cog("Coinflip")

        game = await coinflip.get_coinflip_game(ctx.author)

        if game is None:
            await ctx.send(f"You do not have a coinflip in progress.")
            return

        await coinflip.remove_coinflip(ctx.author)
        await economy.deposit_coins(ctx.author, await game.get_coins())
        await ctx.send(f"Your coinflip has been removed.")