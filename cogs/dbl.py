import discord, json
import dbl as top
from discord.ext import commands, tasks

File = "tools/config.json"
with open(File) as f:
    data = json.load(f)
space = data['SPACE']
topgg = data['TOP']
delly = data['DELLY']

class dbl(commands.Cog):
    '''Discord Bot Lists Commands/Tasks'''
    def __init__(self, bot):
        self.bot = bot
        self.space.start()
        self.delly.start()
        self.dblpy = top.DBLClient(self.bot, topgg, autopost=True)

    def cog_unload(self):
        self.delly.cancel()
        self.space.cancel()

    @tasks.loop(hours=6.0)
    async def space(self):
        '''
        BOTLIST.SPACE
        https://botlist.space
        '''
        headers = {"Authorization": space, "Content-Type": 'application/json'}
        try:
            r = await self.bot.session.post(f"https://api.botlist.space/v1/bots/{self.bot.user.id}", headers=headers, data=json.dumps({'server_count': len(self.bot.guilds)}))
            result = json.loads(await r.text())
            message = result['message']
            c = self.bot.get_channel(803413039256043590)
            await c.send(f"__**BotList.Space**__ - `{message}` **({len(self.bot.guilds)})**")
        except:
            pass

    @tasks.loop(hours=6.0)
    async def delly(self):
        '''
        DISCORDEXTREMELIST.XYZ
        https://discordextremelist.xyz
        '''
        try:
            async with self.bot.session.post(f'https://api.discordextremelist.xyz/v2/bot/{self.bot.user.id}/stats',
            headers={'Authorization': delly, "Content-Type": 'application/json'},
            data=json.dumps({'guildCount': len(self.bot.guilds)})) as r:
                js = await r.json()
            c = self.bot.get_channel(803413039256043590)
            await c.send(f"__**DEL.xyz**__ - Status: `{js['status']}` **({len(self.bot.guilds)})**")
        except:
            pass

    @commands.command()
    async def vcheck(self, ctx, *, member: discord.Member=None):
        if member is None:
            member = ctx.author
        vote = self.dblpy.get_user_vote(member.id)
        if vote:
            status = "✅"
        else:
            status = "❌"
        await ctx.send(f'{status}')
        
def setup(bot):
    bot.add_cog(dbl(bot))
