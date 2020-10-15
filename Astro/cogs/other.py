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
        dice = ['1', '2', '3', '4', '5', '6', 'off the table...']
        await ctx.send(f'The Dice Rolled {random.choice(dice)}')
        
        
        
def setup(bot):
    bot.add_cog(other(bot))
