import discord

from discord import Embed
from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo

import os

import random

import collections

import time, datetime
from datetime import datetime

from multiprocessing.connection import Client

from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

class info(commands.Cog):
    '''Information Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.listcolors = ['0x7289DA', '0x2F3136']
        self.   COLORS = random.choice(listcolors)
        
    @commands.command()
    async def source(self, ctx):
        '''See the bots source'''
        await ctx.send("<:python:758139554670313493> Source: https://asksirk.com/Astro/github.html\nPlease make sure to credit @isirk if you are copying code.")
        
    @commands.command()
    async def about(self, ctx):
        '''Get information about the bot.'''
        infoembed = discord.Embed(title="Info", description="A Utilities Discord Bot with reliability and simplicity", color=self.COLORS)
        infoembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        infoembed.add_field(name= "<:news:758781954073821194> News", value=f"**<:dev:759427919302492160> <@751447995270168586> Is Now PUBLIC! <:dev:759427919302492160>**\nTo invite Sirk click [here](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot).\nOr you can type `{ctx.prefix}invite` to get invite info!", inline=True)
        infoembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758451109919981580.png?v=1")
        infoembed.add_field(name= ":link: Links", value="[Invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&redirect_uri=https%3A%2F%2Fastrobot.carrd.co%2F&response_type=code&scope=bot%20identify)\n[Bot Site](https://asksirk.com/Astro) \n[Github Repository](https://github.com/ISIRK/Astro) \n[Patreon](https://www.patreon.com/Astro_Bot)", inline=False)
        infoembed.set_footer(text="Sirk Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=infoembed)
        
    @commands.command()
    async def credits(self, ctx):
        '''See the credits for Sirk'''
        embed = discord.Embed(title="Credits", description="**<@!542405601255489537> - Developer and Owner**\n**<@!555709231697756160> - API Usage**\n**<@!668906205799907348> - Bot Optimizations**\n**<@!296862365503193098> - Optimizations and Advice**\n", color=0x2F3136)
        await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        supportembed = discord.Embed(title="Support", color=0x2F3136)
        supportembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        supportembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758453150897799172.png?v=1")
        supportembed.add_field(name="Support Server", value="<a:igloading:737723292768796713> Support Server: https://discord.gg/7yZqHfG", inline=False)
        supportembed.add_field(name="Contact", value="To contact dm [isirk#0001](https://discord.com/users/542405601255489537) or email me @ isirk@asksirk.com", inline=False)
        #supportembed.add_field(name=":link: Links", value="Bot Site: https://asksirk.com/Astro\nGithub Repository: https://github.com/ISIRK/Astro\nPatreon: https://www.patreon.com/Astro_Bot", inline=False)
        supportembed.set_footer(text=f"Use {ctx.prefix}help or info for more")
        await ctx.send(embed=supportembed)
    
    @commands.command()
    async def invite(self , ctx):
        '''Get the invite for the bot.'''
        embed = discord.Embed(title="Invite", color=0x2F3136)
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://asksirk.com/Astro/astronaut.jpg")
        embed.add_field(name="Invite Link:", value="🌐 [Invite Link](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot)", inline=False)
        embed.add_field(name="Support Server:", value="<a:igloading:737723292768796713> [Support Server](https://discord.gg/7yZqHfG)", inline=False)
        embed.add_field(name="Contact:", value="To contact dm [isirk#0001](https://discord.com/users/542405601255489537) or email me @ isirk@asksirk.com", inline=False)
        embed.set_footer(text=f"Use {ctx.prefix}help or info for more")
        await ctx.send(embed=embed)
        
    @commands.command()
    async def privacy(self, ctx):
        '''See the bots privacy policy'''
        embed = discord.Embed(title="Privacy Policy for Sirk", description="Sirk strives to store no data to make Sirk as simple to use as possible.\nNothing is stored, recorded or anything of that sort.\n\n<:tab:758139554842148934> [Privacy Policy](https://asksirk.com/Astro/privacy/)", color=0x2F3136)
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Sirk Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=embed)
     
def setup(bot):
    bot.add_cog(info(bot))
