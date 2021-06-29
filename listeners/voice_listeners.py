from discord.ext import commands

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
        pass