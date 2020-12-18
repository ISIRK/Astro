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

from multiprocessing.connection import Client
from random import randint
import discord
from discord.ext import commands
from discord.ext.commands import context
from discord.shard import ShardInfo
from discord.user import User
from discord.utils import get
import os
import collections
import time, datetime
from discord.ext.commands.cooldowns import BucketType
import random
import psutil
import json
import platform
import inspect, sys, multiprocessing, asyncio

from collections import Counter
import time, datetime

from multiprocessing.connection import Client

tools = "tools/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class meta(commands.Cog):
    '''Meta commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        '''Get statistics about the bot.'''
        embed = discord.Embed(title="<a:loading:737722827112972449> Gathering Stats", color=color)
        msg = await ctx.send(embed=embed)
        channel_types = Counter(type(c) for c in self.bot.get_all_channels())
        voice = channel_types[discord.channel.VoiceChannel]
        text = channel_types[discord.channel.TextChannel]
        infoembed = discord.Embed(title="<a:settings:768181060734812230> Stats", description=f"<:member:758139554652749835> Member Count: `{len(self.bot.users)}`\n<:discord:765251798629220382> Servers: `{len(self.bot.guilds)}`\n<:code:758447982688862238> Commands: `{len(self.bot.commands)}`\n<:textchannel:724637677395116072> Channels: `{text}`\n<:voicechannel:724637677130875001> Voice Channels: `{voice}`\n<:dpy:779749503216648233> DPY Version: `{discord.__version__}`\n<:python:758139554670313493> Python Version: `{platform.python_version()}`\n<:server:765946903803854898> Server: `{platform.system()}`\n> Ping:  `{round(self.bot.latency * 1000)}ms`\n> CPU Count: `{multiprocessing.cpu_count()}`\n> CPU Usage: `{psutil.cpu_percent()}%`\n> RAM: `{psutil.virtual_memory().percent}%`", color=color)
        infoembed.set_author(name=ctx.guild.me.name, icon_url=ctx.guild.me.avatar_url)
        infoembed.set_footer(text=footer)
        await asyncio.sleep(2)
        await msg.edit(embed=infoembed)

    @commands.command(aliases=['info', 'i'])
    async def about(self, ctx):
        """Displays bot info"""
        mem = psutil.virtual_memory()
        embed = discord.Embed(title="Bot Info", color=color)
        embed.set_author(name="isirk#0001", icon_url="https://asksirk.com/img/isirk.gif")
        embed.set_footer(text=footer)
        embed.set_thumbnail(url="https://asksirk.com/img/sirk.png")
        embed.add_field(name="About",
                        value=f"A minimalistic bot for discord made by [isirk](https://discord.com/users/542405601255489537)\n[Support Server](https://discord.gg/7yZqHfG)\n[Website](https://asksirk.com/bot/)")
        embed.add_field(name=f"Stats",
                        value=f"Servers: {len(self.bot.guilds)}\nUsers: {len(self.bot.users)}\nCommands: {len(self.bot.commands)}")
        embed.add_field(name="Usage:",
                        value=f"```CPU Usage: {psutil.cpu_percent()}%\n{mem[1] / 1000000} MB available ({100 - mem[2]}%)```",
                        inline=False)
        embed.add_field(name="Version Info",
                        value=f"```Python: {platform.python_version()}\nDiscord.py: {discord.__version__}```")
        embed.add_field(name="Vote!",
                        value="[Top.GG](https://top.gg/bot/751447995270168586/)\n[BotList.Space](https://botlist.space/bot/751447995270168586)\n[Discord Extreme List](https://discordextremelist.xyz/en-US/bots/sirk)")
        await ctx.send(embed=embed)
        
    @commands.command()
    async def credits(self, ctx):
        '''See the credits for Sirk'''
        embed = discord.Embed(title="Credits", description="<@!542405601255489537> (isirk#0001)** - Developer and Owner**\n<@!555709231697756160> (CraziiAce#0001)** - API Usage**\n<@!668906205799907348> (Cyrus#8315)** - Bot Optimizations**\n<@!296862365503193098> (LeSirH#0001)** - Optimizations and Advice**\n<@!345457928972533773> (Moksej#3335)** - Four Lines**", color=color)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def vote(self, ctx):
        embed = discord.Embed(title="Vote", description="[Top.GG](https://top.gg/bot/751447995270168586/)\n[BotList.Space](https://botlist.space/bot/751447995270168586)\n[Discord Extreme List](https://discordextremelist.xyz/en-US/bots/sirk)", color=color)
        embed.set_footer(text=footer)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        await ctx.send('https://discord.gg/7yZqHfG')
    
    @commands.command()
    async def invite(self , ctx):
        '''Get the invite for the bot.'''
        await ctx.message.add_reaction('\U0001f4ec')
        await ctx.author.send('<https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot>')
        
    @commands.command()
    async def privacy(self, ctx):
        '''See the bots privacy policy'''
        embed = discord.Embed(title="Privacy Policy for Sirk Bot", url="https://asksirk.com/bot/privacy/", color=color)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def donate(self, ctx):
        message = "Thank you for choosing to donate. It is greatly appreciated."
        await ctx.send(embed=discord.Embed(title=message, url=f"https://donatebot.io/checkout/743121194911531110?buyer={ctx.author.id}", color=color))

    @commands.command()
    async def ping(self, ctx):
        '''Get the bot ping'''
        await ctx.message.add_reaction('🏓')
        await ctx.send(f"Pong! Average Latency is {round(self.bot.latency * 1000)} ms")
        
    @commands.command()
    async def uptime(self, ctx):
        """Displays the uptime"""
        delta_uptime = datetime.datetime.utcnow() - self.bot.start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"Been up for {days}d, {hours}h, {minutes}m, {seconds}s")

    @commands.command()
    async def server(self, ctx):
        '''Get information about the server.'''

        statuses = collections.Counter([m.status for m in ctx.guild.members])

        embed = discord.Embed(title=f"{ctx.guild.name}", color=color)
        embed.description = ctx.guild.description if ctx.guild.description else None
        embed.add_field(name='**General:**',
                        value=f'Owner: **{ctx.guild.owner}**\n'
                              f'Created on: **{datetime.datetime.strftime(ctx.guild.created_at, "%A %d %B %Y at %H:%M")}**\n'
                              f'<:member:758139554652749835> **{ctx.guild.member_count}**\n'
                              f'<:online:758139458767290421> **{statuses[discord.Status.online]:,}**\n'
                              f'<:idle:758139458406711307> **{statuses[discord.Status.idle]:,}**\n'
                              f'<:dnd:758139458598993921> **{statuses[discord.Status.dnd]:,}**\n'
                              f'<:offline:758139458611970088> **{statuses[discord.Status.offline]:,}**\n'
                              f'<:boost4:724328585137225789> **Tier {ctx.guild.premium_tier}**\n'
                              f'Region: **{ctx.guild.region}**\n'
                              f'Boosters: **{ctx.guild.premium_subscription_count}**\n'
                              f'Max File Size: **{round(ctx.guild.filesize_limit / 1048576)} MB**\n'
                              f'Bitrate: **{round(ctx.guild.bitrate_limit / 1000)} kbps**\n'
                              f'Max Emojis: **{ctx.guild.emoji_limit}**\n', inline=False)

        embed.add_field(name='**Channel Information:**',
                        value=f'AFK timeout: **{int(ctx.guild.afk_timeout / 60)}m**\n'
                              f'AFK channel: **{ctx.guild.afk_channel}**\n'
                              f'<:textchannel:724637677395116072> **{len(ctx.guild.text_channels)}**\n'
                              f'<:voicechannel:724637677130875001> **{len(ctx.guild.voice_channels)}**\n', inline = False)

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url=ctx.guild.banner_url)
        embed.set_footer(text=f'Guild ID: {ctx.guild.id} | {footer}')

        return await ctx.send(embed=embed)

    @commands.command(aliases=['whois', 'ui'])
    async def user(self, ctx, *, member: discord.Member = None):
        '''Get information about the mentioned user.'''
        if member is None:
            member = ctx.author

        if len(member.activities) > 0:
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    activity = 'Listening to `Spotify`'
                elif isinstance(activity, discord.Game):
                    activity = f'Playing `{activity.name}``'
                elif isinstance(activity, discord.Streaming):
                    activity = f'Streaming `{activity.name}`'
                else:
                    activity = '`None`'
        else:
            activity = '`None`'
        statuses = {
                    "online": "<:online:758139458767290421>",
                    "idle": "<:idle:758139458406711307>",
                    "dnd": "<:dnd:758139458598993921>",
                    "offline": "<:offline:758139458611970088>"
                    }
        roles = ' '.join([r.mention for r in member.roles if r != ctx.guild.default_role] or ['None'])
        shared = sum(g.get_member(member.id) is not None for g in self.bot.guilds)
                
        embed = discord.Embed(title=f"{member}", color=member.color)
        embed.add_field(name='**General:**',
                        value=f'Name: `{member}`\n' 
                              f'Status: {statuses[str(member.status)]}\n'
                              f'Bot: `{member.bot}`\n'
                              f'Shared Guilds: `{shared}`\n'
                              f'Account Created on: `{datetime.datetime.strftime(member.created_at, "%A %d %B %Y at %H:%M")}`', inline=False)

        embed.add_field(name='**Guild related information:**',
                        value=f'Joined guild: `{datetime.datetime.strftime(member.joined_at, "%A %d %B %Y at %H:%M")}`\n'
                              f'Nickname: `{member.nick}`\n'
                              f'Roles: {roles}', inline=False)

        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Member ID: {member.id} | {footer}')

        return await ctx.send(embed=embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, member: discord.Member=None): # set the member object to None
        '''Get the avatar of the mentioned member.'''
        if not member: # if member is no mentioned
            member = ctx.message.author # set member as the author
        userAvatar = member.avatar_url
        avatarembed = discord.Embed(color=0x2F3136)
        avatarembed.set_author(name=member)
        avatarembed.set_image(url=userAvatar)
        await ctx.send(embed=avatarembed)
                        
    @commands.command(name="perms")
    async def permissions(self, ctx, *, member: discord.Member=None):
        '''A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked.'''

        if not member:
            member = ctx.author

        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions', description=f"```yaml\n{perms}```", colour=color)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.set_footer(text=footer)
        await ctx.send(content=None, embed=embed)
                        
def setup(bot):
    bot.add_cog(meta(bot))
