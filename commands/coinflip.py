import discord
from discord.ext import commands
from decouple import config
import typing
import datetime
import asyncio

class CoinflipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._coinflip_open_message = None
        self._coinflip_results_message = None

    @commands.command(name = "setup")
    async def on_setup_coinflip_command(self, ctx):
        await ctx.message.delete()
        coinflip_cog = self.bot.get_cog("Coinflip")
        self._coinflip_results_message = await ctx.send(embed=coinflip_cog.get_coinflip_results_message())
        self._coinflip_open_message = await ctx.send(embed=coinflip_cog.get_open_coinflips_message())

    @commands.command(name = "create", aliases=["c"])
    async def on_create_coinflip_command(self, ctx, coins: int):
        if ctx.channel.name == config('coinflip_channel_name'):
            await ctx.message.delete()
            economy_cog = self.bot.get_cog("Economy")
            coinflip_cog = self.bot.get_cog("Coinflip")
            #Get the users wallet/coins
            wallet = economy_cog.get_wallet(ctx.author)
            
            if coins <= 0:
                await ctx.send(f"> {ctx.author.mention}, you cannot create a zero/negative value coinflip.", delete_after=5)
            elif wallet < coins:
                await ctx.send(f"> {ctx.author.mention}, you do not have enough coins for this coinflip.", delete_after=5)
            elif wallet >= coins:
                economy_cog.withdraw(ctx.author, coins)
                coinflip_cog.create_coinflip(ctx.author, coins)
                await self.reset_messages()

    @commands.command(name = "join", aliases=["j"])
    async def on_join_coinflip_command(self, ctx, member: discord.Member):
        if ctx.channel.name == config('coinflip_channel_name'):
            if member.name != ctx.author.name:
                await ctx.message.delete()
                economy_cog = self.bot.get_cog("Economy")
                coinflip_cog = self.bot.get_cog("Coinflip")

                coinflip_match = coinflip_cog.get_coinflip_game(member)
                if coinflip_match is None:
                    await ctx.send(f"> {ctx.author.mention}, a game by that user does not exist.", delete_after=5)
                    return

                if not coinflip_match.is_joinable():
                    await ctx.send(f"> {ctx.author.mention}, you cannot join that game.", delete_after=5)
                    return

                wallet = economy_cog.get_wallet(ctx.author)
                if wallet < coinflip_match.get_coins():
                    await ctx.send(f"> {ctx.author.mention}, you do not have enough coins to join this coinflip.", delete_after=5)
                    return

                economy_cog.withdraw(ctx.author, coinflip_match.get_coins())
                coinflip_cog.join_coinflip(member, ctx.author)
                coinflip_cog.run_coinflip(coinflip_match.get_creator())
                economy_cog.deposit(coinflip_match.get_winner(), int(coinflip_match.get_coins() * 1.7))
                economy_cog._jackpot += int(coinflip_match.get_coins() * 0.3)
                await self.reset_messages()
            else:
                await ctx.message.delete()
                await ctx.send(f"> {ctx.author.mention}, you cannot stake yourself.", delete_after=5)
                
    @commands.command(name = "remove", aliases=["r"])
    async def on_remove_coinflip_command(self, ctx):
        if ctx.channel.name == config('coinflip_channel_name'):
            await ctx.message.delete()
            economy_cog = self.bot.get_cog("Economy")
            coinflip_cog = self.bot.get_cog("Coinflip")

            coinflip_match = coinflip_cog.get_coinflip_game(ctx.author)

            if coinflip_match is None:
                await ctx.send(f"> {ctx.author.mention}, you do not have a coinflip in progress.", delete_after=5)
                return

            coinflip_cog.remove_coinflip(ctx.author)
            economy_cog.deposit(ctx.author, coinflip_match.get_coins())
            await self.reset_messages()

    @commands.command(name = "wl", aliases=["winlose"])
    async def on_win_lose_command(self, ctx):
        if ctx.channel.name == config('coinflip_channel_name'):
            await ctx.message.delete()
            coinflip_cog = self.bot.get_cog("Coinflip")

            wins = len([x for x in coinflip_cog.get_coinflips() if x.get_winner() == ctx.author])
            lose = len([x for x in coinflip_cog.get_coinflips() if x.get_loser() == ctx.author])
            await ctx.send(f"> {ctx.author.mention}, your win/lose is: {wins}/{lose}.", delete_after=5)

            await self.reset_messages()

    async def reset_messages(self):
        coinflip_cog = self.bot.get_cog("Coinflip")
        asyncio.create_task(self._coinflip_results_message.edit(embed=coinflip_cog.get_coinflip_results_message()))
        asyncio.create_task(self._coinflip_open_message.edit(embed=coinflip_cog.get_open_coinflips_message()))