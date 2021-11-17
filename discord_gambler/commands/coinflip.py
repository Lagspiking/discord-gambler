import discord
from discord.ext import commands
from decouple import config
from discord_gambler import _coinflip_channel, _guild_id
import typing
import datetime
import asyncio
import os
from random import randrange


class CoinflipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_cog = self.bot.get_cog("Economy")
        self.coinflip_cog = self.bot.get_cog("Coinflip")
        self._coinflip_open_message = None
        self._coinflip_results_message = None

    @commands.command(name="setup")
    async def on_setup_coinflip_command(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            self._coinflip_results_message = await ctx.send(
                embed=self.coinflip_cog.get_coinflip_results_message()
            )
            self._coinflip_open_message = await ctx.send(
                embed=self.coinflip_cog.get_open_coinflips_message()
            )

    @commands.command(name="create", aliases=["c"])
    async def on_create_coinflip_command(self, ctx, coins):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            coinflip_cog = self.bot.get_cog("Coinflip")
            #If user already has a coinflip open, don't allow another one
            if coinflip_cog.get_coinflip_game(ctx.author):
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you already have a coinflip in progress.",
                        color=discord.Color.red(),
                    ), delete_after=5,
                )
                return

            thousands = coins.count("k")
            coins = int("".join([x for x in coins if x.isdigit()]))
            for x in range(0, thousands):
                coins = int(coins * 1000)

            # Get the users wallet/coins
            wallet = self.economy_cog.get_wallet(ctx.author)

            if coins <= 0:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you cannot create a zero/negative value coinflip.",
                        color=discord.Color.red(),
                    ), delete_after=5,
                )
            elif wallet < coins:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you do not have enough coins for this coinflip.",
                        color=discord.Color.red(),
                    ), delete_after=5,
                )
            elif wallet >= coins:
                coinflip_cog.create_coinflip(ctx.author, coins)
                await self.reset_messages()

    @commands.command(name="join", aliases=["j"])
    async def on_join_coinflip_command(self, ctx, member: discord.Member):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            if member.name != ctx.author.name:
                coinflip_match = self.coinflip_cog.get_coinflip_game(member)
                if coinflip_match is None:
                    await ctx.send(
                        embed=discord.Embed(
                            title="Error",
                            description=f"{ctx.author.mention}, a game by that user does not exist.",
                            color=discord.Color.red(),
                        ), delete_after=5,
                    )
                    return

                if not coinflip_match.is_joinable():
                    await ctx.send(
                        embed=discord.Embed(
                            title="Error",
                            description=f"{ctx.author.mention}, you cannot join that game.",
                            color=discord.Color.red(),
                        ), delete_after=5,
                    )
                    return

                wallet = self.economy_cog.get_wallet(ctx.author)
                if wallet < coinflip_match.get_coins():
                    #Easter egg
                    rand = randrange(25)
                    message = f"{ctx.author.mention}, you do not have enough coins to join this coinflip."
                    if rand == 0:
                        message += " Lmfao, imagine being poor."
                    await ctx.send(
                        embed=discord.Embed(
                            title="Error",
                            description=message,
                            color=discord.Color.red(),
                        ), delete_after=5,
                    )
                    return

                self.coinflip_cog.join_coinflip(member, ctx.author)
                self.coinflip_cog.run_coinflip(coinflip_match.get_creator())
                await self.reset_messages()
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you cannot stake yourself.",
                        color=discord.Color.red(),
                    ), delete_after=5,
                )

    @commands.command(name="remove", aliases=["r"])
    async def on_remove_coinflip_command(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            coinflip_match = self.coinflip_cog.get_coinflip_game(ctx.author)

            if coinflip_match is None:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you do not have a coinflip in progress.",
                        color=discord.Color.red(),
                    ), delete_after=5,
                )
                return

            self.coinflip_cog.remove_coinflip(ctx.author)
            await self.reset_messages()

    @commands.command(name="wl", aliases=["winloss"])
    async def on_win_loss_command(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            wins = len(
                [
                    x
                    for x in self.coinflip_cog.get_coinflips()
                    if x.get_winner() == ctx.author
                ]
            )
            loss = len(
                [x for x in self.coinflip_cog.get_coinflips() if x.get_loser() == ctx.author]
            )
            await ctx.send(
                embed=discord.Embed(
                    title="Information",
                    description=f"{ctx.author.mention}, your win/loss is: {wins}/{loss}.",
                    color=discord.Color.green(),
                ), delete_after=5,
            )
            await self.reset_messages()

    @commands.command(name="reset")
    async def on_reset_command(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            await self.reset_messages()

    async def reset_messages(self):
        await asyncio.create_task(
            self._coinflip_results_message.edit(
                embed=self.coinflip_cog.get_coinflip_results_message()
            )
        )
        await asyncio.create_task(
            self._coinflip_open_message.edit(
                embed=self.coinflip_cog.get_open_coinflips_message()
            )
        )
