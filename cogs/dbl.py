import discord, json
from discord.ext import commands, tasks

class dbl(commands.Cog):
    '''Discord Bot Lists Commands/Tasks'''
    def __init__(self, bot):
        self.bot = bot
        self.space.start()
        
    @tasks.loop(seconds=30.0)
    async def space(self):
        '''
        BOTLIST.SPACE
        https://botlist.space
        '''
        url = "https://api.botlist.space/v1/bots/751447995270168586"
        token = "24981b666bc4a21833e516dba8da3760bea7f55b23613d6ddb85baacaec11e94cfca11893250be38fd4684bb1fcefaa9"
        headers = {"Authorization": token, "Content-Type": 'application/json'}
        try:
            r = await self.bot.session.post(url, headers=headers, data=json.dumps({'server_count': len(self.bot.guilds)}))
            result = json.loads(await r.text())
            message = result['message']
            c = self.bot.get_channel(793312077083181080)
            await c.send(f"{message} **({len(self.bot.guilds)})**")
            print(f"{message} **({len(self.bot.guilds)})**")
        except Exception as e:
            print(e)
        
def setup(bot):
    bot.add_cog(dbl(bot))
