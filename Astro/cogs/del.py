import discord, aiohttp, json
from discord.ext import tasks, commands

class DEL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.del_update_stats.start()

    def cog_unload(self):
        self.del_update_stats.cancel()

    @tasks.loop(minutes=30.0)
    async def del_update_stats(self):
        """ This automatically updates your server count to Discord Extreme List every 30 minutes. """
        await self.bot.wait_until_ready()
        async with aiohttp.ClientSession() as session:
            async with session.post(f'https://api.discordextremelist.xyz/v2/bot/{self.bot.user.id}/stats',
            headers={'Authorization': 'DELAPI_63c6a6c40c666a6c1213187d8db52940-751447995270168586', # Make sure you put your API Token Here
            "Content-Type": 'application/json'},
            data=json.dumps({'guildCount': len(self.bot.guilds)# Remove this line if you don't have shards on your bot
            })) as r:
                js = await r.json()
                if js['error'] == True:
                    print(f'Failed to post to discordextremelist.xyz\n{js}')

def setup(bot):
    bot.add_cog(DEL(bot))
