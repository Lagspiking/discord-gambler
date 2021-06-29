import discord
from discord.ext import commands

class TestCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Create a command with aliases
    @commands.command(name = "test", aliases=["test2", "test3"])
    async def on_test_command(self, ctx):
        print("on_test_command")

    #Create a command with optional parameters (!optional_parameters @Sparks 1000)
    @commands.command(name="optional_parameters")
    async def on_optional_parameters(self, ctx, member: discord.Member, hotdogs: int):
        print(f"{member.display_name} has {hotdogs} hotdogs!")

    #Event is triggered when ANY command is completed - We should probably add a check
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print("on_command_completion")
