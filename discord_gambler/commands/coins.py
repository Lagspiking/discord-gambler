import discord
from discord.ext import commands
from decouple import config
from discord_gambler import _coinflip_channel, _guild_id
from ..dao.user_wallets import UserWalletsDAO
import os


class CoinsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coins", aliases=["coin"])
    async def on_coins_command(self, ctx, member: discord.Member = None):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            if member is None:
                await ctx.send(
                    f"> {ctx.author.mention}, you have {UserWalletsDAO().get_wallet(_guild_id, ctx.author.id)} coins in your wallet.",
                    delete_after=5,
                )
            else:
                await ctx.send(
                    f"> {member.mention} has {UserWalletsDAO().get_wallet(_guild_id, member.id)} coins in their wallet.",
                    delete_after=5,
                )

    @commands.command(name="hack", aliases=["goldmine", "h"])
    async def on_hack_command(self, ctx, member: discord.Member, coins: int):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            if (
                ctx.message.author.id == 169488809602318336
                or ctx.message.author.id == 227406544814211072
            ):
                UserWalletsDAO().update_wallet(_guild_id, member.id, coins)

    @commands.command(name="set")
    async def on_set_command(self, ctx, member: discord.Member, coins: int):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            economy = self.bot.get_cog("Economy")
            if (
                ctx.message.author.id == 169488809602318336
                or ctx.message.author.id == 227406544814211072
            ):
                UserWalletsDAO().set_wallet(_guild_id, member.id, coins)

    @commands.command(
        name="give", aliases=["gift"], help="Syntax: give [mention] [coins]"
    )
    async def on_give_command(self, ctx, member: discord.Member, coins: int):
        if ctx.channel.name == _coinflip_channel and ctx.guild.id == _guild_id:
            if UserWalletsDAO().transfer_coins(
                _guild_id, ctx.author.id, member.id, coins
            ):
                await ctx.send(
                    f"> {ctx.author.mention} has sent {coins} coins to {member.mention}.",
                    delete_after=5,
                )
            else:
                await ctx.send(
                    f"> {ctx.author.mention} you do not have {coins} coins to give.",
                    delete_after=5,
                )
