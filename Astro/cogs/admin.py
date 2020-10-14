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



class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
        
def setup(bot):
    bot.add_cog(admin(bot))