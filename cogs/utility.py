from multiprocessing.connection import Client
from random import randint
import discord
from discord.ext import commands
from discord.ext.commands import context
from discord.shard import ShardInfo
from discord.user import User
from discord.utils import get
from datetime import datetime
import os
import collections
import time, datetime
from discord.ext.commands.cooldowns import BucketType
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
import random
import psutil
import json
import platform

tools = "/home/pi/Discord/Sirk/utils/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class utility(commands.Cog):
    '''Utility commands'''
    def __init__(self, bot):
        self.bot = bot

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

        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url=ctx.guild.banner_url)
        embed.set_footer(text=f'Guild ID: {ctx.guild.id} | {footer}')

        return await ctx.send(embed=embed)

    @commands.command()
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
        embed = discord.Embed(title=f"{member}", color=color)
        embed.add_field(name='**General:**',
                        value=f'Name: `{member}`\n' 
                              f'Status: {statuses[str(member.status)]}\n'
                              f'Bot: `{member.bot}`\n'
                              f'Account Created on: `{datetime.datetime.strftime(member.created_at, "%A %d %B %Y at %H:%M")}`', inline=False)

        embed.add_field(name='**Guild related information:**',
                        value=f'Joined guild: `{datetime.datetime.strftime(member.joined_at, "%A %d %B %Y at %H:%M")}`\n'
                              f'Nickname: `{member.nick}`\n'
                              f'Roles: {roles}', inline=False)

        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Member ID: {member.id} | {footer}')

        return await ctx.send(embed=embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, member: discord.Member=None): # set the member object to None
        '''Get the avatar of the mentioned member.'''
        if not member: # if member is no mentioned
            member = ctx.message.author # set member as the author
        userAvatar = member.avatar_url
        avatarembed = discord.Embed(color=color)
        avatarembed.set_author(name=member) #, icon_url=ctx.author.avatar_url
        avatarembed.set_image(url=userAvatar)
        await ctx.send(embed=avatarembed)
                        
    @commands.command(name="perms")
    async def permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions', description=f"```yaml\n{perms}```", colour=color)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.set_footer(text=footer)
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(utility(bot))
