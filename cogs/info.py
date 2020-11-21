import discord

from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo

import os

import json

import inspect

import random

import collections

import time, datetime
from datetime import datetime

from multiprocessing.connection import Client

from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

colorfile = "/home/pi/Discord/Sirk/utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)

class info(commands.Cog):
    '''Information Commands'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def vote(self, ctx):
        '''Vote for Sirk Bot on top.gg'''
        embed=discord.Embed(title="Vote", description="**Vote for Sirk Bot [here](https://top.gg/bot/751447995270168586/vote)**\nHave a cookie as well -> [🍪](https://orteil.dashnet.org/cookieclicker/)", color=color)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def about(self, ctx):
        '''Get information about the bot.'''
        infoembed = discord.Embed(title="Info", description="A Minimalist Discord Bot with reliability and simplicity", color=color)
        infoembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        infoembed.add_field(name= "<:news:758781954073821194> News", value=f"**🎧 <@751447995270168586> Has music commands! 🎧**\n> To see the music commands use `{ctx.prefix}help music`!", inline=True)
        infoembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758451109919981580.png?v=1")
        infoembed.add_field(name= ":link: Links", value="[Invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot)\n[Website](https://asksirk.com/bot) \n[Github Repository](https://github.com/ISIRK/Sirk)", inline=False)
        infoembed.set_footer(text="Sirk Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=infoembed)
        
    @commands.command()
    async def credits(self, ctx):
        '''See the credits for Sirk'''
        embed = discord.Embed(title="Credits", description="<@!542405601255489537> (isirk#0001)** - Developer and Owner**\n<@!555709231697756160> (CraziiAce#0001)** - API Usage**\n<@!668906205799907348> (Cyrus#8315)** - Bot Optimizations**\n<@!296862365503193098> (LeSirH#0001)** - Optimizations and Advice**\n<@!345457928972533773> (Moksej#3335)** - One Line**", color=color)
        await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        await ctx.send('https://discord.gg/7yZqHfG')
    
    @commands.command()
    async def invite(self , ctx):
        '''Get the invite for the bot.'''
        await ctx.send('<https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot>')
        
    @commands.command()
    async def privacy(self, ctx):
        '''See the bots privacy policy'''
        embed = discord.Embed(title="Privacy Policy for Sirk", description="[Privacy Policy](https://asksirk.com/bot/privacy/)", color=color)
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Sirk Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=embed)
     
def setup(bot):
    bot.add_cog(info(bot))
