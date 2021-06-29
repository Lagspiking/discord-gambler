from pymongo import MongoClient
from discord.ext import commands
from decouple import config

class DatabaseCog(commands.Cog, name = "Database"):
    def __init__(self, bot):
        self._client = MongoClient(config("mongo_db"))

    