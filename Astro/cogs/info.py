from multiprocessing.connection import Client
import discord
from discord import Embed
from discord.ext import commands
from discord.shard import ShardInfo
from discord.user import User
from discord.utils import get
from datetime import datetime
import os
import collections
import time, datetime

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        '''Get information about the bot.'''
        infoembed = discord.Embed(title="<:info:758451109919981580> Info", description="A Utilities Discord Bot with reliability and simplicity", color=0x7289DA)
        infoembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        infoembed.add_field(name= "<:check:758363543002808371> Updates", value="Version 1.0 \n<:translate:758449663517917195> Translators Needed.\nIf you can speak another language fluently or know someone who can DM isirk#001.", inline=True)
        infoembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758451109919981580.png?v=1")
        infoembed.add_field(name= ":link: Links", value="[Bot Site](https://asksirk.com/Astro) \n[Github Repository](https://github.com/ISIRK/Astro) \n[Patreon](https://www.patreon.com/Astro_Bot)")
        infoembed.add_field(name="About", value="<:code:758447982688862238> Made with :heart: in <:python:758139554670313493>\nOwned, Developed, and Run by isirk#0001", inline=False)
        infoembed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=infoembed)

    @commands.command()
    async def help1(self, ctx):
        '''Old/New help command that is being worked on right now.'''
        helpembed = discord.Embed(title="Help", description="A Utilities Discord Bot with reliability and simplicity\n Made By isirk#0001", color=0x7289DA)
        helpembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        helpembed.add_field(name="Prefix", value="`^` (Not Customizeable)", inline=False)
        helpembed.add_field(name="Bot", value="`help`\n`info`\n`ping`\n`support`")
        helpembed.add_field(name="Mod", value="`kick`\n`ban`\n`mute`\n`unmute`")
        helpembed.add_field(name="Utility", value="`avatar`\n`slowmode`\n`clear`\n`server`\n`user`")
        helpembed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")

        await ctx.send(embed=helpembed)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        supportembed = discord.Embed(title="Support", color=0x7289DA)
        supportembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        supportembed.add_field(name=":link: Links", value="[Bot Site](https://asksirk.com/Astro) \n[Github Repository](https://github.com/ISIRK/Astro) \n[Patreon](https://www.patreon.com/Astro_Bot)", inline=True)
        supportembed.add_field(name="Contact", value="To contact dm isirk#0001 or email me @ isirk@asksirk.com", inline=True)
        supportembed.set_footer(text="Use [prefix] help or info.")
        await ctx.send(embed=supportembed)
    
    @commands.command()
    async def credits(self , ctx):
        '''Get the credits of the bot.'''
        embed = discord.Embed(title="Credits", color=0x7289DA)
        embed.add_field(name="Bot Maker", value="isirk", inline=False)
        embed.add_field(name="Coder", value="isirk\nThe source code is here --> https://github.com/ISIRK/Astro", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(info(bot))
