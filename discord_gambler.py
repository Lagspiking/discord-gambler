import os
import discord
from decouple import config

class DiscordClient(discord.Client):
    async def on_ready(self):
        print("on_ready")

    async def on_message(self, message):
        #Check if author is a bot
        if message.author == client.user or message.author.bot:
            return
        print("on_message")

if __name__ == "__main__":
    #Implement .env
    _token = config("discord_token")
    intents = discord.Intents.default()
    intents.members = True
    client = DiscordClient(intents=intents)
    client.run(_token)