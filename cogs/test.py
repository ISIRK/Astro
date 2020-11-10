import discord, json

from discord.user import User
from discord.ext import menus
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import context
from discord.ext.commands.cooldowns import BucketType

from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

colorfile = "/home/pi/Discord/Sirk/utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)

class MySource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=4)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))
    
class Test:
    def __init__(self, key, value):
        self.key = key
        self.value = value

data = [
    Test(key=key, value=value)
    for key in ['test', 'other', 'okay']
    for value in range(20)
]

class Source(menus.GroupByPageSource):
    async def format_page(self, menu, entry):
        joined = '\n'.join(f'{i}. <Test value={v.value}>' for i, v in enumerate(entry.items, start=1))
        return f'**{entry.key}**\n{joined}\nPage {menu.current_page + 1}/{self.get_max_pages()}'
    
class Embeds(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=4)

    async def format_page(self, menu, entries):
        embeds = [
            discord.Embed(title="test0", description="test as well", color=color),
            discord.Embed(title="test1", description="test as well", color=color),
            discord.Embed(title="test2", description="test as well", color=color)
        ]

class test(commands.Cog):
    '''Testing Commands'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def menu(self, ctx):
        pages = menus.MenuPages(source=MySource(range(1, 100)), clear_reactions_after=True)
        await pages.start(ctx)
    @commands.command()
    async def menu_source(self, ctx):
        pages = menus.MenuPages(source=Embeds(data, key=lambda t: t.key, per_page=12), clear_reactions_after=True)
        await pages.start(ctx)
     
    @commands.command()
    async def paginate(self, ctx):
        embeds = [
            discord.Embed(title="test page 1", description="This is just some test content!", color=color),
            discord.Embed(title="test page 2", description="Nothing interesting here.", color=color),
            discord.Embed(title="test page 3", description="Why are you still here?", color=color)
        ]

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()
    
    @commands.command()
    async def choice(self, ctx):
        multiple_choice = BotMultipleChoice(ctx, ['one', 'two', 'three', 'four', 'five', 'six'], "Testing stuff")
        await multiple_choice.run()

        await multiple_choice.quit(multiple_choice.choice)
      
    @commands.command()
    async def confirm(self, ctx):
        confirmation = BotConfirmation(ctx, color)
        await confirmation.confirm("Are you sure?")

        if confirmation.confirmed:
            await confirmation.update("Confirmed", color=color)
        else:
            await confirmation.update("Not confirmed", hide_author=True, color=color)

        
def setup(bot):
    bot.add_cog(test(bot))
