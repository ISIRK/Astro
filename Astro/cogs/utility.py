from multiprocessing.connection import Client
import discord
from discord import Embed
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

class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server(self, ctx):
        '''Get information about the server.'''

        statuses = collections.Counter([m.status for m in ctx.guild.members])

        embed = discord.Embed(title=f"{ctx.guild.name}", color=0x7289DA)
        embed.description = ctx.guild.description if ctx.guild.description else None
        embed.add_field(name='**General:**',
                        value=f'Owner: **{ctx.guild.owner}**\n'
                              f'Created on: **{datetime.datetime.strftime(ctx.guild.created_at, "%A %d %B %Y at %H:%M")}**\n'
                              f'<:member:758139554652749835> **{ctx.guild.member_count}**\n'
                              f'<:online:758139458767290421> **{statuses[discord.Status.online]:,}**\n'
                              f'<:idle:758139458406711307> **{statuses[discord.Status.idle]:,}**\n'
                              f'<:dnd:758139458598993921> **{statuses[discord.Status.dnd]:,}**\n'
                              f'<:offline:758139458611970088> **{statuses[discord.Status.offline]:,}**\n'
                              f'<:boost:758139554778578954> **Tier {ctx.guild.premium_tier}**\n'
                              f'Region: **{ctx.guild.region}**\n'
                              f'Boosters: **{ctx.guild.premium_subscription_count}**\n'
                              f'Max File Size: **{round(ctx.guild.filesize_limit / 1048576)} MB**\n'
                              f'Bitrate: **{round(ctx.guild.bitrate_limit / 1000)} kbps**\n'
                              f'Max Emojis: **{ctx.guild.emoji_limit}**\n', inline=False)

        embed.add_field(name='**Channel Information:**',
                        value=f'`AFK timeout:` **{int(ctx.guild.afk_timeout / 60)}m**\n'
                              f'`AFK channel:` **{ctx.guild.afk_channel}**\n'
                              f'`Text channels:` **{len(ctx.guild.text_channels)}**\n'
                              f'`Voice channels:` **{len(ctx.guild.voice_channels)}**\n', inline = False)

        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url=ctx.guild.banner_url)
        embed.set_footer(text=f'Guild ID: {ctx.guild.id}')

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
        embed = discord.Embed(title=f"{member}", color=0x7289DA)
        embed.add_field(name='**General:**',
                        value=f'Name: `{member}`\n'
                              f'Desktop Status: `{member.desktop_status}`\n'
                              f'Mobile Status: `{member.mobile_status}`\n'
                              f'Browser Status: `{member.web_status}`\n'
                              f'Account Created on: `{datetime.datetime.strftime(member.created_at, "%A %d %B %Y at %H:%M")}`', inline=False)

        embed.add_field(name='**Guild related information:**',
                        value=f'Joined guild: `{datetime.datetime.strftime(member.joined_at, "%A %d %B %Y at %H:%M")}`\n'
                              f'Nickname: `{member.nick}`\n'
                              f'Top role: {member.top_role.mention}', inline=False)

        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Member ID: {member.id}')

        return await ctx.send(embed=embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, member: discord.Member=None): # set the member object to None
        '''Get the avatar of the mentioned member.'''
        if not member: # if member is no mentioned
            member = ctx.message.author # set member as the author
        userAvatar = member.avatar_url
        avatarembed = discord.Embed(title=f"Avatar for {member}", color=0x7289DA)
        avatarembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        avatarembed.set_image(url=userAvatar)
        await ctx.send(embed=avatarembed)

    @commands.command()
    async def ping(self, ctx):
        '''Get the bot ping'''
        pingembed = discord.Embed(color=0x7289DA)
        pingembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        pingembed.add_field(name="Pong!", value=f'```autohotkey\n{round(self.bot.latency * 1000)} ms```')
        await ctx.send(embed=pingembed)

    @commands.command()
    async def stats(self ,ctx):
        '''Get the bot stats'''
        await ctx.send(f'Astro is serving {len(self.bot.users)} users in {len(self.bot.guilds)} guilds.')

    @commands.command()
    async def contact(self , ctx, *, content):
        '''Send a support notice'''
        embed = discord.Embed(color=0x7289DA)
        embed.set_author(name=f"Sent from {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Message:", value=f'{content}')
        u = self.bot.get_user(542405601255489537)
        await u.send(embed=embed)
        await ctx.send(f"<:check:758363543002808371> Message sent to {u}")



def setup(bot):
    bot.add_cog(utility(bot))
