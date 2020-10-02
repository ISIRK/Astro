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
    @commands.is_owner()
    @commands.command(aliases=['sl'])
    async def status_listening(self, ctx, *, status):
        '''Change listening Status'''
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
        await ctx.send(f'<:online:758139458767290421> Changed status to `Listening {status}`')
    @commands.is_owner()
    @commands.command(aliases=['online'])
    async def status_online(self, ctx):
        '''Change status to online'''
        await self.bot.change_presence(status=discord.Status.online)
        await ctx.send(f'Changed status to <:online:758139458767290421>')
    
    async def do_rtfm(self, ctx, key, obj):
        page_types = {
            'latest': 'https://discordpy.readthedocs.io/en/latest',
            'latest-jp': 'https://discordpy.readthedocs.io/ja/latest',
            'python': 'https://docs.python.org/3',
            'python-jp': 'https://docs.python.org/ja/3',
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, '_rtfm_cache'):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)

        if key.startswith('latest'):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == '_':
                    continue
                if q == name:
                    obj = f'abc.Messageable.{name}'
                    break

        cache = list(self._rtfm_cache[key].items())
        def transform(tup):
            return tup[0]

        matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        e = discord.Embed(colour=discord.Colour.blurple())
        if len(matches) == 0:
            return await ctx.send('Could not find anything. Sorry.')

        e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
        await ctx.send(embed=e)

        if ctx.guild and ctx.guild.id in (DISCORD_API_ID, DISCORD_PY_GUILD):
            query = 'INSERT INTO rtfm (user_id) VALUES ($1) ON CONFLICT (user_id) DO UPDATE SET count = rtfm.count + 1;'
            await ctx.db.execute(query, ctx.author.id)

    def transform_rtfm_language_key(self, ctx, prefix):
        if ctx.guild is not None:
            #                             日本語 category
            if ctx.channel.category_id == 490287576670928914:
                return prefix + '-jp'
            #                    d.py unofficial JP
            elif ctx.guild.id == 463986890190749698:
                return prefix + '-jp'
        return prefix

    @commands.group(aliases=['rtfd'], invoke_without_command=True)
    async def rtfm(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a discord.py entity.
        Events, objects, and functions are all supported through a
        a cruddy fuzzy algorithm.
        """
        key = self.transform_rtfm_language_key(ctx, 'latest')
        await self.do_rtfm(ctx, key, obj)
        
def setup(bot):
    bot.add_cog(admin(bot))
