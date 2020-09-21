from multiprocessing.connection import Client
import discord
from discord import Embed
from discord.ext import commands
from discord.shard import ShardInfo
from discord.user import User
from discord.utils import get
import os

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
        helpembed.add_field(name="Info", value="@Astro Mention Me for Info")
        helpembed.add_field(name="Prefix", value="`^` (Not Customizeable)", inline=False)
        helpembed.add_field(name="Bot", value="`help`\n`info`\n`ping`")
        helpembed.add_field(name="Mod", value="`kick`\n`ban`\n`mute`\n`unmute`")
        helpembed.add_field(name="Utility", value="`avatar`\n`slowmode`\n`clear`")
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
        pingembed.add_field(name="Pong!", value=f'```{round(self.bot.latency * 1000)}ms```')
        await ctx.send(embed=pingembed)

def setup(bot):
    bot.add_cog(Bot_Cmds(bot))