from discord.ext import commands
import json



class SaveCommand(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._economy_cog = self._bot.get_cog("Economy")
        self._coinflip_cog = self._bot.get_cog("Coinflip")
        self._save_state = {}

    @commands.command(name="save", aliases=["s"])
    async def on_save_command(self, ctx):
        self._save_state['wallets'] = self._economy_cog.get_all_wallets()
        self._save_state['current_jackpot'] = self._economy_cog.get_jackpot()
        # self._save_state['jackpot_eligable'] = self._economy_cog.get_jackpot_eligable()
        # self._save_state['coinflip_games'] = self._coinflip_cog.get_coinflips()
        
        #TODO: Handle saving and loading within a cog
        with open('save.json', 'w') as outfile:
            json.dump(self._save_state, outfile, sort_keys=True, indent=4)

    @commands.command(name="load", aliases=["l"])
    async def on_load_command(self, ctx):
        with open('save.json') as outfile:
            data = json.load(outfile)
            self._economy_cog.set_all_wallets(data['wallets'])
            self._economy_cog.set_jackpot(data['current_jackpot'])
            # self._economy_cog.set_jackpot_eligable(data['jackpot_eligable'])