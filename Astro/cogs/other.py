import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import context
from discord.shard import ShardInfo
from discord.user import User
from discord.utils import get

import time, datetime
from datetime import datetime

import os

import random

import collections





class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def dice(self, ctx):
        foo = ['a', 'b', 'c', 'd', 'e']
        await ctx.send(random.choice(foo))
        
        
        
def setup(bot):
    bot.add_cog(other(bot))
