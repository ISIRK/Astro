import discord, json
import subprocess as sp
from discord.ext import commands, menus

tools = "/home/pi/Discord/Sirk/utils/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)


# ext-menus paginator
class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        return await channel.send(f'Hello {ctx.author}')

    @menus.button('\N{THUMBS UP SIGN}')
    async def on_thumbs_up(self, payload):
        await self.message.edit(content=f'Thanks {self.ctx.author}!')

    @menus.button('\N{THUMBS DOWN SIGN}')
    async def on_thumbs_down(self, payload):
        await self.message.edit(content=f"That's not nice {self.ctx.author}...")

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()
        
# ext-menus Embed paginator
class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, embed):
        return embed
    
class test(commands.Cog, command_attrs=dict(hidden=True)):
    '''Testing Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, title, *options):
        '''Make a quick poll'''
        reactions = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"}
        s = ""
        num = 1
        for i in options: 
            s += f"{num} - {i}\n" 
            num += 1
        embed = discord.Embed(title = title, description = s, color=color)
        embed.set_footer(text=footer)
        try:
            await ctx.channel.purge(limit=1)
        except:
            pass
        msg = await ctx.send(embed=embed)
        for i in range(1, len(options) + 1): await msg.add_reaction(reactions[i])
            
    @commands.command()
    async def menu(self, ctx):
        m = MyMenu()
        await m.start(ctx)
    
    @commands.command()
    async def emenu(self, ctx):
        embeds = [
            discord.Embed(title="Embed"),
            discord.Embed(title="Another embed"),
            discord.Embed(title="Some other embed")
        ]
        menu = menus.MenuPages(EmbedPageSource(embeds, per_page=1))
        await menu.start(ctx)

    coglist = [self.bot.cogs[i] for i in self.bot.cogs]
    d = {}
    for i in coglist:
      d.update({f"{i.qualified_name}": [f"`{j.name}` ({j.signature})\n{j.help}\n" for j in i.get_commands()]})

    class Test:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    data = [
        Test(key=key, value=value)
        for key in d.keys()
        for value in d[key]
    ]

    class Source(menus.GroupByPageSource):
        async def format_page(self, menu, entry):
            joined = '\n'.join(f'{v.value}' for i, v in enumerate(entry.items, start=1))
            return discord.Embed(title = entry.key, description = joined).set_footer(text = f"{menu.current_page + 1}/{self.get_max_pages()}")
    
    @commands.command()
    async def phelp(self, ctx):
        pages = menus.MenuPages(source=Source(data, key=lambda t: t.key, per_page=12), clear_reactions_after=True)
        await pages.start(ctx)
        
def setup(bot):
    bot.add_cog(test(bot))
