import discord
from discord import Embed

from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import bot

import os

import psutil

import collections

import time, datetime
from datetime import datetime

from multiprocessing.connection import Client

from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def leaveguild(self, ctx):
        '''Leave the current server.'''
        embed=discord.Embed(title='Goodbye', color=0x2F3136)
        await ctx.send(embed=embed)
        await ctx.guild.leave()
    
    @commands.is_owner()
    @commands.command()
    async def status(self, ctx, type, emoji=None, *, status=None):
        '''Change the Bot Status'''
        if type == "playing":
            await self.bot.change_presence(activity=discord.Game(name=f"{status}", emoji=f"{emoji}"))
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
            await ctx.send(f'<:online:758139458767290421> Changed status to `Streaming {status}`')
        elif type == "reset":
            await self.bot.change_presence(status=discord.Status.online)
            await ctx.send("<:online:758139458767290421> Reset Status")
        else:
            await ctx.send("Type needs to be either `playing|listening|watching|streaming|competing|bot|reset`")

    @commands.is_owner()
    @commands.command()
    async def dm(self , ctx, user : discord.Member, *, content):
        '''Dm a Member'''
        embed = discord.Embed(color=0x2F3136)
        embed.set_author(name=f"Sent from {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Message:", value=f'{content}')
        embed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/726779670514630667.png?v=1")
        await user.send(embed=embed)
        await ctx.send(f"<:comment:726779670514630667> Message sent to {user}")
   
    @commands.is_owner()
    @commands.command()
    async def say(self, ctx, *, content:str):
            await ctx.send(content)
        
    @commands.is_owner()
    @commands.command()
    async def dev(self, ctx):

        dev = discord.Embed(title="Dev", description="Developer Commands\n***Note Only the Bot Owner Can Use These***", color=0x2F3136)
        dev.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        dev.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        dev.add_field(name="Syntax:", value="```yaml\n<input> - Input for the Command\n[o] - Optional\n```", inline=False)
        dev.add_field(name="Commands:", value="`jsk` - Jishaku\n`dm <user> <message>` - Dm the mentioned User from the Server.\n`leaveguild` - Leave the current server\n`status <type> <[o]status>` - Change the bot status.\n`say <message>` - Make the bot say a message.", inline=False)

        jsk = discord.Embed(title="jsk", description="Commands:\ncancel - Cancels a task with the given index.\ncat - Read out a file, using syntax highlighting if detected.\ncurl - Download and display a text file from the internet.\ndebug - Run a command timing execution and catching exceptions.\ngit - Shortcut for 'jsk sh git'. Invokes the system shell.\nhide - Hides Jishaku from the help command.\nin - Run a command as if it were run in a different channel.\nload - Loads or reloads the given extension names.\npy - Direct evaluation of Python code.\npy - inspect Evaluation of Python code with inspect information.\nrepeat - Runs a command multiple times in a row.\nretain - Turn variable retention for REPL on or off.\nshell - Executes statements in the system shell.\nshow - Shows Jishaku in the help command.\nshutdown - Logs this bot out.\nsource - Displays the source code for a command.\nsu - Run a command as someone else.\nsudo - Run a command bypassing all checks and cooldowns.\ntasks - Shows the currently running jishaku tasks.\nunload - Unloads the given extension names.\nvoice - Voice-related commands.", color=0x2F3136)

        embeds = [
            dev,
            jsk
        ]

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()
        
            
def setup(bot):
    bot.add_cog(dev(bot))
