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

class Bot_Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        infoembed = discord.Embed(title="Info", description="A Utilities Discord Bot with reliability and simplicity", color=0x7289DA)
        infoembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        infoembed.add_field(name= "<:tabs:752603220945141852> Updates", value="Version 0.9 \n<:status_online:752277014668640296> Finished info, help, ping, kick, ban, avatar, mention, slowmode, clear commands \n<:status_idle:752277014651863070> Making welcome-leave message\n<:status_dnd:752277014345678989> Future things are reaction roles and modlog", inline=True)
        infoembed.add_field(name= ":link: Links", value="[Bot Site](https://asksirk.com/Astro) \n[Github Repository](https://github.com/ISIRK/Astro) \n[Patreon](https://www.patreon.com/Astro_Bot)")
        infoembed.add_field(name="About", value="<:python:757007320621252619> Made in Python with :heart: by isirk#0001", inline=False)
        infoembed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=infoembed)

    @commands.command()
    async def help(self, ctx):
        helpembed = discord.Embed(title="Help", description="A Utilities Discord Bot with reliability and simplicity\n Made By isirk#0001", color=0x7289DA)
        helpembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        helpembed.add_field(name="Prefix", value="`^` (Not Customizeable)", inline=False)
        helpembed.add_field(name="Bot", value="`help`\n`info`\n`ping`\n`support`")
        helpembed.add_field(name="Mod", value="`kick`\n`ban`\n`mute`\n`unmute`")
        helpembed.add_field(name="Utility", value="`avatar`\n`slowmode`\n`clear`\n`server`\n`user`")
        helpembed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")

        await ctx.send(embed=helpembed)

    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member=None): # set the member object to None
        if not member: # if member is no mentioned
            member = ctx.message.author # set member as the author
        userAvatar = member.avatar_url
        avatarembed = discord.Embed(title=f"Avatar for {member}", color=0x7289DA)
        avatarembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        avatarembed.set_image(url=userAvatar)
        await ctx.send(embed=avatarembed)

    @commands.command()
    async def ping(self, ctx):
        pingembed = discord.Embed(color=0x7289DA)
        pingembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        pingembed.add_field(name="Pong!", value=f'```autohotkey\n{round(self.bot.latency * 1000)} ms```')
        await ctx.send(embed=pingembed)

    @commands.command()
    async def server(self, ctx):
        '''Get information about the server.'''

        statuses = collections.Counter([m.status for m in ctx.guild.members])

        embed = discord.Embed(title=f"{ctx.guild.name}", color=0x7289DA)
        embed.description = ctx.guild.description if ctx.guild.description else None
        embed.add_field(name='**General:**',
                        value=f'Owner: **{ctx.guild.owner}**\n'
                              f'Created on: **{datetime.datetime.strftime(ctx.guild.created_at, "%A %d %B %Y at %H:%M")}**\n'
                              f'<:member:757763257497813052> **{ctx.guild.member_count}**\n'
                              f'<:status_online:752277014668640296> **{statuses[discord.Status.online]:,}**\n'
                              f'<:status_idle:752277014651863070> **{statuses[discord.Status.idle]:,}**\n'
                              f'<:status_dnd:752277014345678989> **{statuses[discord.Status.dnd]:,}**\n'
                              f'<:offline:757759505009475634> **{statuses[discord.Status.offline]:,}**\n'
                              f'<:7485_server_boost:757763282072371300> **Tier {ctx.guild.premium_tier}**\n'
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
                              f'Account Created on: `{datetime.datetime.strftime(member.created_at, "%A %d %B %Y at %H:%M")}`', inline=False)

        embed.add_field(name='**Guild related information:**',
                        value=f'Joined guild: `{datetime.datetime.strftime(member.joined_at, "%A %d %B %Y at %H:%M")}`\n'
                              f'Nickname: `{member.nick}`\n'
                              f'Top role: {member.top_role.mention}', inline=False)

        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Member ID: {member.id}')

        return await ctx.send(embed=embed)

    
    @commands.is_owner()
    @commands.command()
    async def guilds(self, ctx):
        guildsembed = discord.Embed(title="Guilds", color=0x7289DA)

        for guild in self.bot.guilds:
            guildsembed.add_field(name=f'{guild.name}', value=f'`{guild.owner}`'f'<@!{guild.owner_id}>')
        await ctx.send(embed=guildsembed)

    @commands.command()
    async def support(self, ctx):
        supportembed = discord.Embed(title="Support", color=0x7289DA)
        supportembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        supportembed.add_field(name=":link: Links", value="[Bot Site](https://asksirk.com/Astro) \n[Github Repository](https://github.com/ISIRK/Astro) \n[Patreon](https://www.patreon.com/Astro_Bot)", inline=True)
        supportembed.add_field(name="Contact", value="To contact dm isirk#0001 or email me @ isirk@asksirk.com", inline=True)
        supportembed.set_footer(text="Use [prefix] help or info.")
        await ctx.send(embed=supportembed)

    @commands.is_owner()
    @commands.command()
    async def leaveguild(self, ctx):
        embed=discord.Embed(title='Goodbye', color=0x7289DA)
        await ctx.send(embed=embed)
        await ctx.guild.leave()
    
    @commands.command()
    async def credits(self , ctx):
        embed = discord.Embed(title="Credits", color=0x7289DA)
        embed.add_field(name="Bot Maker", value="isirk", inline=False)
        embed.add_field(name="Coder", value="isirk\nThe source code is here --> https://github.com/ISIRK/Astro", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Bot_Cmds(bot))