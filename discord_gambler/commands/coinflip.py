import random
import discord
from discord.ext import commands
from decouple import config
from discord_gambler import _coinflip_channel, _guild_id
from ..dao.user_wallets import UserWalletsDAO
from ..dao.coinflips import CoinflipsDAO
import asyncio
from random import randrange


class CoinflipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coinflip_cog = self.bot.get_cog("Coinflip")
        self._coinflip_open_message = None
        self._coinflip_results_message = None
        self._giveaway_tax = 0.25

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
            # If user already has a coinflip open, don't allow another one
            if CoinflipsDAO().get_open_coinflip(ctx.author.id):
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you already have a coinflip in progress.",
                        color=discord.Color.red(),
                    ),
                    delete_after=5,
                )
                return

            thousands = coins.count("k")
            coins = int("".join([x for x in coins if x.isdigit()]))
            for x in range(0, thousands):
                coins = int(coins * 1000)

            # Get the users wallet/coins
            wallet = UserWalletsDAO().get_wallet(ctx.author.id)

            if coins <= 0:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you cannot create a zero/negative value coinflip.",
                        color=discord.Color.red(),
                    ),
                    delete_after=5,
                )
            elif wallet < coins:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you do not have enough coins for this coinflip.",
                        color=discord.Color.red(),
                    ),
                    delete_after=5,
                )
            elif wallet >= coins:
                UserWalletsDAO().update_wallet(ctx.author.id, -coins)
                CoinflipsDAO().create_coinflip(ctx.author.id, coins)
                await self.reset_messages()

    @commands.command(name="join", aliases=["j"])
    async def on_join_coinflip_command(self, ctx, member: discord.Member):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            if member.name != ctx.author.name:
                if not CoinflipsDAO().get_open_coinflip(member.id):
                    await ctx.send(
                        embed=discord.Embed(
                            title="Error",
                            description=f"{ctx.author.mention}, a game by that user does not exist.",
                            color=discord.Color.red(),
                        ),
                        delete_after=5,
                    )
                    return

                wallet = UserWalletsDAO().get_wallet(ctx.author.id)
                coinflip_value = CoinflipsDAO().get_open_coinflip(member.id)[1]
                if wallet < coinflip_value:
                    # Easter egg
                    rand = randrange(25)
                    message = f"{ctx.author.mention}, you do not have enough coins to join this coinflip."
                    if rand == 0:
                        message += " Lmfao, imagine being poor."
                    await ctx.send(
                        embed=discord.Embed(
                            title="Error",
                            description=message,
                            color=discord.Color.red(),
                        ),
                        delete_after=5,
                    )
                    return

                UserWalletsDAO().update_wallet(ctx.author.id, -coinflip_value)
                CoinflipsDAO().accept_coinflip(member.id, ctx.author.id)
                total_stake = coinflip_value * 2
                coinflip = random.choice([0, 1])

                if coinflip == 0:
                    CoinflipsDAO().finish_coinflip(
                        member.id, ctx.author.id, ctx.author.id, member.id
                    )
                    UserWalletsDAO().update_wallet(ctx.author.id, total_stake)
                else:
                    CoinflipsDAO().finish_coinflip(
                        member.id, ctx.author.id, member.id, ctx.author.id
                    )
                    UserWalletsDAO().update_wallet(member.id, total_stake)

                await self.reset_messages()

            else:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you cannot stake yourself.",
                        color=discord.Color.red(),
                    ),
                    delete_after=5,
                )

    @commands.command(name="remove", aliases=["r"])
    async def on_remove_coinflip_command(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            coinflip = CoinflipsDAO().get_open_coinflip(ctx.author.id)
            if coinflip is None:
                await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description=f"{ctx.author.mention}, you do not have a coinflip in progress.",
                        color=discord.Color.red(),
                    ),
                    delete_after=5,
                )
            else:
                CoinflipsDAO().remove_coinflip(ctx.author.id)
                UserWalletsDAO().update_wallet(ctx.author.id, coinflip[1])
                await self.reset_messages()

    @commands.command(name="wl", aliases=["winloss"])
    async def on_win_loss_command(self, ctx):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            wins = CoinflipsDAO().get_won_games(ctx.author.id)
            loss = CoinflipsDAO().get_lost_games(ctx.author.id)
            await ctx.send(
                embed=discord.Embed(
                    title="Information",
                    description=f"{ctx.author.mention}, your win/loss is: {wins}/{loss}.\n Your win rate is {wins/(wins+loss)*100}% or {wins/(wins+loss)}",
                    color=discord.Color.green(),
                ),
                delete_after=5,
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
