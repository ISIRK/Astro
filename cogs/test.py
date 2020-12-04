import discord, json, aiohttp
import subprocess as sp
from discord.ext import commands, menus

tools = "json/tools.json"
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
    
    @commands.command(aliases=["g"])
    async def google(self, ctx, *, query: str):
        """Searches google for a given query."""

        async with google_search(query) as results:
            embeds = []

            for result in results:
                embed = Embed.default(ctx)
                embed.title = result.title
                embed.description = result.snippet
                embed.url = result.link
                embed.set_image(url=result.image if result.image is not None
                                    and result.image.startswith(("https://", "http://"))
                                    else discord.Embed.Empty)
                print(result.link)

                embeds.append(embed)

            menu = menus.MenuPages(EmbedMenu(embeds), clear_reactions_after=True)
            await menu.start(ctx)
    
        
def setup(bot):
    bot.add_cog(test(bot))
