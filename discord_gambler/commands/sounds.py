import discord
from discord.ext import commands
from decouple import config
from asyncio import sleep
import random
import glob

class SoundsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="sounds")
    async def on_sounds_command(self, ctx):
        message = "Type _!playsound [name]_ to play a sound in a channel. \n"
        sounds = glob.glob("sounds/*.mp3")

        for sound in sounds:
            message += "> " + sound.replace("sounds\\", "").replace(".mp3", "\n")

        await ctx.send(message)


    @commands.command(name="playsound")
    async def on_playsound_command(self, ctx, sound):

        if ctx.author.voice is None or ctx.author.voice.channel is None:
            return

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client
        
        vc.play(discord.FFmpegPCMAudio(executable="libs/ffmpeg.exe", source=f"sounds\\{sound}.mp3"))
        vc.source = discord.PCMVolumeTransformer(vc.source, volume=0.5)
        while vc.is_playing():
            await sleep(1)

        await vc.disconnect()