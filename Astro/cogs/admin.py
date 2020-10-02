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

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def guilds(self, ctx):
        '''Get the guilds the bot is in.'''
        guildsembed = discord.Embed(title="Guilds", color=0x7289DA)

        for guild in self.bot.guilds:
            guildsembed.add_field(name=f'{guild.name}', value=f'`{guild.owner}`'f'<@!{guild.owner_id}>')
        await ctx.send(embed=guildsembed)

    @commands.is_owner()
    @commands.command()
    async def leaveguild(self, ctx):
        '''Leave the current server.'''
        embed=discord.Embed(title='Goodbye', color=0x7289DA)
        await ctx.send(embed=embed)
        await ctx.guild.leave()
    
    @commands.is_owner()
    @commands.command(aliases=['sp'])
    async def status_playing(self, ctx, *, status):
        '''Change playing Status'''
        await self.bot.change_presence(activity=discord.Game(name=f"{status}"))
        await ctx.send(f'<:online:758139458767290421> Changed status to `Playing {status}`')
    @commands.is_owner()
    @commands.command(aliases=['sw'])
    async def status_watching(self, ctx, *, status):
        '''Change watching Status'''
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))
        await ctx.send(f'<:online:758139458767290421> Changed status to `Watching {status}`')
    @commands.is_owner()
    @commands.command(aliases=['sb'])
    async def status_bot(self, ctx):
        '''Change the bot status to bot stats'''
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"{len(self.bot.users)} users"))
        await ctx.send(f'<:online:758139458767290421> Changed status to `Watching {len(self.bot.users)} users`')
        #guilds;  [in {len(self.bot.guilds)} guilds]
    
def setup(bot):
    bot.add_cog(admin(bot))
