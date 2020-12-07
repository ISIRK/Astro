import discord

from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import bot

import os

import io

import json

import psutil

import aiohttp

import collections

import time, datetime
from datetime import datetime

from multiprocessing.connection import Client

import subprocess as sp

from jishaku.codeblocks import codeblock_converter

tools = "json/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)


class dev(commands.Cog):
    '''Developer Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    
    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, name: str):
        """Loads an extension. """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
        await ctx.send(f"📥 Loaded extension **`cogs/{name}.py`**")

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, name: str):
        """Reloads an extension. """

        try:
            self.bot.reload_extension(f"cogs.{name}")
            await ctx.send(f"🔁 Reloaded extension **`cogs/{name}.py`**")

        except Exception as e:
            return await ctx.send(f"```py\n{e}```")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, name: str):
        """Unloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
        await ctx.send(f"📤 Unloaded extension **`cogs/{name}.py`**")
    
    @commands.is_owner()
    @commands.command(aliases=['ra'])
    async def reloadall(self, ctx):
        """Reloads all extensions. """
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    return await ctx.send(f"```py\n{e}```")

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        await ctx.send("**🔁 `Reloaded All Extentions`**")

    @commands.command(aliases=['s'])
    @commands.is_owner()
    async def sync(self, ctx):
        """Sync with GitHub and reload all the cogs"""
        embed = discord.Embed(title="Syncing...", description="<a:loading:737722827112972449> Syncing and reloading cogs.", color=color)
        msg = await ctx.send(embed=embed)
        async with ctx.channel.typing():
            output = sp.getoutput('git pull')
        embed = discord.Embed(title="Synced", description="<a:Animated_Checkmark:726140204045303860> Synced with GitHub and reloaded all the cogs.", color=color)
        # Reload Cogs as well
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    return await ctx.send(f"```py\n{e}```")

        if error_collection:
            err = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{err}"
            )

        await msg.edit(embed=embed)
    
    # Do not use because of ram usage, cuz it does not kill what is running.
    '''@commands.is_owner()
    @command.command()
    async def restart(self, ctx):
        output = sp.getoutput('python3 sirk.py &')
        await ctx.bot.logout()'''

    @commands.is_owner()
    @commands.command()
    async def leaveguildanddontchokeisirk(self, ctx):
        '''Leave the current server.'''
        embed=discord.Embed(title='Goodbye', color=color)
        await ctx.send(embed=embed)
        await ctx.guild.leave()


    @commands.is_owner()
    @commands.command()
    async def status(self, ctx, type, *, status=None):
        '''Change the Bot Status'''
        if type == "playing":
            await self.bot.change_presence(activity=discord.Game(name=f"{status}"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Playing {status}`')
        elif type == "listening":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Listening to {status}`')
        elif type == "watching":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Watching {status}`')
        elif type == "bot":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"{len(self.bot.users)} users in {len(self.bot.guilds)} servers"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Watching {len(self.bot.users)} users in {len(self.bot.guilds)} servers`')
        elif type == "competing":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"{status}"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Competing in {status}`')
        elif type == "streaming":
            await self.bot.change_presence(activity=discord.Streaming(name=f"{status}", url="https://www.twitch.tv/isirk"))
            await ctx.send(f'<:streaming:769640090275151912> Changed status to `Streaming {status}`')
        elif type == "reset":
            await self.bot.change_presence(status=discord.Status.online)
            await ctx.send("<:online:758139458767290421> Reset Status")
        else:
            await ctx.send("Type needs to be either `playing|listening|watching|streaming|competing|bot|reset`")

    @commands.is_owner()
    @commands.command()
    async def dm(self , ctx, user : discord.Member, *, content):
        '''Dm a Member'''
        embed = discord.Embed(color=color)
        embed.set_author(name=f"Sent from {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Message:", value=f'{content}')
        embed.set_footer(text=footer)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/726779670514630667.png?v=1")
        await user.send(embed=embed)
        await ctx.send(f"<:comment:726779670514630667> Message sent to {user}")
        
    @commands.is_owner()
    @commands.command(aliases = ["ss"])
    async def screenshot(self, ctx, url):
        embed = discord.Embed(title = f"Screenshot of {url}", color=color)
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}') as r:
                res = await r.read()
            embed.set_image(url="attachment://ss.png")
            embed.set_footer(text=footer)
            await ctx.send(file=discord.File(io.BytesIO(res), filename="ss.png"), embed=embed)
    
    @commands.is_owner()
    @commands.command()
    async def say(self, ctx, *, content:str):
        '''Make the bot say something'''
        await ctx.send(content)
          
    @commands.is_owner()
    @commands.command(aliases=['e'])
    async def eval(self, ctx, *, code: str):
        '''Evaluate code'''
        cog = self.bot.get_cog("Jishaku")
        res = codeblock_converter(code)
        await cog.jsk_python(ctx, argument=res)

    @commands.is_owner()
    @commands.command()
    async def sudo(self, ctx, *, command:str):
        '''Sudo command'''
        cog = self.bot.get_cog("Jishaku")
        await cog.jsk_sudo(ctx, command_string=command)
        
    @commands.is_owner()
    @commands.command()
    async def nick(self, ctx, *, name: str):
        try:
            await ctx.guild.me.edit(nick=name)
            await ctx.send(f"Successfully changed username to **{name}**")
        except discord.HTTPException as err:
            await ctx.send(f"```{err}```")
            
    @commands.is_owner()
    @commands.command()
    async def rn(self, ctx):
        await ctx.guild.me.edit(nick=None)
        await ctx.send(f'Nickname reset to Sirk')
        
    @commands.is_owner()
    @commands.command()
    async def cogs(self, ctx):
        s = ""
        for cog in self.bot.cogs.keys():
            s += f"\n {cog}"
        embed = discord.Embed(title = "Active Cogs:", description = f"```yaml\n{s}```", color=color)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)
        
    def is_me(m):
        return m.author == self.bot.user

    @commands.is_owner()    
    @commands.command(aliases=['bc'])
    async def cleanup(self, ctx, *, number : int):
        deleted = await ctx.channel.purge(limit=number, check=is_me)
        await channel.send('Deleted {} message(s)'.format(len(deleted)))
    
def setup(bot):
    bot.add_cog(dev(bot))
