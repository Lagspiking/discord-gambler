from discord.ext import commands
import discord
from asyncio import sleep
import random
import glob

#https://discordpy.readthedocs.io/en/stable/api.html#event-reference
class VoiceListeners(commands.Cog):
    
    def __init__(self, bot):
        self._bot = bot

    #Called when a Member changes their VoiceState.
    #The following, but not limited to, examples illustrate when this event is called:
    #A member joins a voice channel.
    #A member leaves a voice channel.
    #A member is muted or deafened by their own accord.
    #A member is muted or deafened by a guild administrator.
    #This requires Intents.voice_states to be enabled.
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #If a user has joined a voice chat NOT moved voice chat
        #TODO: Scrape sounds from a website/stream them instead
        if not before.channel and after.channel:
            vc = await after.channel.connect()
            voice_channel = after.channel.guild.voice_client

            voice_channel.play(discord.FFmpegPCMAudio(executable="libs/ffmpeg.exe", source=random.choice(glob.glob("sounds/*.mp3"))))
            vc.source = discord.PCMVolumeTransformer(vc.source, volume=0.5)
            while vc.is_playing():
                await sleep(1)

            await vc.disconnect()