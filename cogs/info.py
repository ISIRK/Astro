import discord

from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo

import os, json, inspect, random, collections, platform, sys, psutil

import time, datetime
from datetime import datetime

from multiprocessing.connection import Client

from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

tools = "/home/pi/Discord/Sirk/utils/tools.json"
with open(tools) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)
footer = data['FOOTER']

class info(commands.Cog):
    '''Information Commands'''
    def __init__(self, bot):
        self.bot = bot
    
    '''@commands.Cog.listener()
    async def on_message(self):
        if message.content.endswith('@Sirk'):
            embed = discord.Embed(title="Sirk Bot", description="Hey there :wave: Seems like you mentioned me.\n\nMy prefixes are: `sirk `, `Sirk `, `@Sirk ` and `^`\nIf you would like to see my commands type `[prefix]help`", color=0x2F3136)
            await message.channel.send(embed=embed)'''
        
    @commands.command()
    async def vote(self, ctx):
        '''Vote for Sirk Bot on top.gg'''
        embed=discord.Embed(title="Vote", description="**Vote for Sirk Bot [here](https://top.gg/bot/751447995270168586/vote)**\nHave a cookie as well -> [🍪](https://orteil.dashnet.org/cookieclicker/)")
        await ctx.send(embed=embed)
        
    @commands.command()
    async def about(self, ctx):
        '''Get information about the bot.'''
        infoembed = discord.Embed(title="Sirk Bot", description="A minimalistic bot for discord\nDeveloped by [isirk](https://discord.com/users/542405601255489537)", color=color)
        infoembed.add_field(name= "<:news:758781954073821194> News", value=f"**🎧 <@751447995270168586> Has music commands! 🎧**\n> To see the music commands use `{ctx.prefix}help music`!", inline=True)
        infoembed.add_field(name="<a:settings:768181060734812230> Stats", value=f"<:member:758139554652749835> Member Count: `{len(self.bot.users)}`\n<:discord:765251798629220382> Servers: `{len(self.bot.guilds)}`\n<:code:758447982688862238> Commands: `{len(self.bot.commands)}`\n<:dpy:779749503216648233> DPY Version: `{discord.__version__}`\n<:python:758139554670313493> Python Version: `{platform.python_version()}`\n<:server:765946903803854898> Server: `{platform.system()}`\n> CPU Usage: `{psutil.cpu_percent()}%`\n> RAM USAGE: `{psutil.virtual_memory().percent}%`", inline=False)
        infoembed.add_field(name= ":link: Links", value="[Invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot)\n[Website](https://asksirk.com/bot)", inline=False)
        infoembed.set_thumbnail(url="https://asksirk.com/img/sirk.png")
        infoembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        infoembed.set_footer(text=footer)
        await ctx.send(embed=infoembed)
        
    @commands.command()
    async def credits(self, ctx):
        '''See the credits for Sirk'''
        embed = discord.Embed(title="Credits", description="<@!542405601255489537> (isirk#0001)** - Developer and Owner**\n<@!555709231697756160> (CraziiAce#0001)** - API Usage**\n<@!668906205799907348> (Cyrus#8315)** - Bot Optimizations**\n<@!296862365503193098> (LeSirH#0001)** - Optimizations and Advice**\n<@!345457928972533773> (Moksej#3335)** - One Line**", color=color)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        await ctx.send('https://discord.gg/7yZqHfG')
    
    @commands.command()
    async def invite(self , ctx):
        '''Get the invite for the bot.'''
        await ctx.author.send('<https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot>')
        
    @commands.command()
    async def privacy(self, ctx):
        '''See the bots privacy policy'''
        embed = discord.Embed(title="Privacy Policy for Sirk", description="[Privacy Policy](https://asksirk.com/bot/privacy/)", color=color)
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        '''Get the bot ping'''                        
        pingembed = discord.Embed(title="Pong!", color=color)
        pingembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        pingembed.add_field(name="<:server:765946903803854898> Server", value=f'```autohotkey\n{round(self.bot.latency * 1000)} ms```')
                        
        start = time.perf_counter()
        message = await ctx.send("Pinging...")
        end = time.perf_counter()
        duration = (end - start) * 1000
                        
        pingembed.add_field(name="<a:typing:765946280601059349> Typing", value='```autohotkey\n{:.2f} ms```'.format(duration))
        pingembed.set_footer(text=footer)
        await message.edit(embed=pingembed)

     
def setup(bot):
    bot.add_cog(info(bot))
