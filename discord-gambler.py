import os
import discord

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
    _token = "ODU5MDc1Mzg0ODc2MjA0MDMy.YNnaTA.3RaNWfzY3uuJFCVML20Baucp5WM"
    intents = discord.Intents.default()
    intents.members = True
    client = DiscordClient(intents=intents)
    client.run(_token)