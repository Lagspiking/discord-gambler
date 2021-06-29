import discord
from discord.ext import commands
from decouple import config
import typing
import datetime

class CoinflipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "create", aliases=["c"])
    async def on_create_coinflip_command(self, ctx, coins: int):
        if ctx.channel.name == config('channel_name'):
            await ctx.message.delete()
            economy_cog = self.bot.get_cog("Economy")
            coinflip_cog = self.bot.get_cog("Coinflip")
            
            embed = discord.Embed(title=f"Coinflip", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.set_author(name="Lagspike™")
            embed.add_field(name="**__User__**", value=f"{ctx.author.mention}", inline=True)
            embed.add_field(name="**vs**", value=f"1000 coins", inline=True)
            embed.add_field(name="**__User__**", value=f"Joinable", inline=True)
            embed.set_footer(text=f"Made by Nrwls & Sparks")
            #Get the users wallet/coins
            wallet = economy_cog.get_wallet(ctx.author)
            
            if coins <= 0:
                await ctx.send(f"You cannot create a zero/negative value coinflip.")
            elif wallet < coins:
                await ctx.send(f"You do not have enough coins for this coinflip.")
            elif wallet >= coins:
                economy_cog.withdraw(ctx.author, coins)
                coinflip_cog.create_coinflip(ctx.author, coins)
                await ctx.send(embed=embed)

    @commands.command(name = "join", aliases=["j"])
    async def on_join_coinflip_command(self, ctx, member: discord.Member):
        if ctx.channel.name == config('channel_name'):
            await ctx.message.delete()
            economy_cog = self.bot.get_cog("Economy")
            coinflip_cog = self.bot.get_cog("Coinflip")

            coinflip_match = coinflip_cog.get_coinflip_game(member)
            if coinflip_match is None:
                await ctx.send(f"A game by that user does not exist.")
                return

            if not coinflip_match.is_joinable():
                await ctx.send(f"That game is not joinable.")
                return

            wallet = economy_cog.get_wallet(ctx.author)
            if wallet < coinflip_match.get_coins():
                await ctx.send(f"You do not have enough coins to join this coinflip.")
                return

            economy_cog.withdraw(ctx.author, coinflip_match.get_coins())
            coinflip_cog.join_coinflip(member, ctx.author)
            coinflip_cog.run_coinflip(coinflip_match.get_creator())
            economy_cog.deposit(coinflip_match.get_winner(), coinflip_match.get_coins() * 2)
            await ctx.send(f"{coinflip_match.get_winner()} has won {coinflip_match.get_coins()} coins from {coinflip_match.get_loser()}")

    @commands.command(name = "remove", aliases=["r"])
    async def on_remove_coinflip_command(self, ctx):
        if ctx.channel.name == config('channel_name'):
            await ctx.message.delete()
            economy_cog = self.bot.get_cog("Economy")
            coinflip_cog = self.bot.get_cog("Coinflip")

            coinflip_match = coinflip_cog.get_coinflip_game(ctx.author)

            if coinflip_match is None:
                await ctx.send(f"You do not have a coinflip in progress.")
                return

            coinflip_cog.remove_coinflip(ctx.author)
            economy_cog.deposit(ctx.author, coinflip_match.get_coins())
            await ctx.send(f"Your coinflip has been removed.")