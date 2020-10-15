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
        embed = discord.Embed(title="Dice", description=f'The Dice Rolled {random.choice(dice)}', color=0x2F3136)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758138226874908705/766312838910181421/unknown.png")
        await ctx.send(embed=embed)
        
        
        
def setup(bot):
    bot.add_cog(other(bot))
