'''

MIT License

Copyright (c) 2020 isirk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

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

def setup(bot):
    bot.add_cog(test(bot))
