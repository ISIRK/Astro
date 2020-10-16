import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import context
from discord.ext.commands.cooldowns import BucketType
from discord.shard import ShardInfo
from discord.user import User
from discord.utils import get

import time, datetime
from datetime import datetime

import os

import random

import collections

import asyncio


class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def dice(self, ctx):
        dice = ['1', '2', '3', '4', '5', '6', 'off the table...\n*You Found The Mystery!*']
        embed = discord.Embed(title="Dice", description=f'The Dice Rolled {random.choice(dice)}', color=0x2F3136)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758138226874908705/766312838910181421/unknown.png")
        await ctx.send(embed=embed)
        
        
    '''@commands.command()
    async def quest(self, ctx):
        await ctx.send("Quest Started!\nQuestion 1: `What is 128+289?`\nType you answer below")
        try:
            q1 = await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await ctx.send('Timeout Error')
        else: 
            if q1.content != "417":
                await ctx.send("Correct!\nQuestion 2: `How many letters are in the alphabet?\nType you answer below")
                q2 = await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
                if q2.content == "26":
                    await ctx.send("Correct!")
                else:
                    await ctx.send("Incorrect.")
            else:
                await ctx.send("Incorrect.")'''
       
    @commands.command(name='???')
    @commands.cooldown(1,60,BucketType.user) 
    async def questtest(self, ctx):
        
        start = time.perf_counter()
        end = time.perf_counter()
        duration = (end - start)
        
        await ctx.send("Quest Started!\n**Question 1: `What is 128+289?`**\nType you answer below")
        try:
            q1 = await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await ctx.send('Timeout Error')
        else:
            if q1.content != "417":
                await ctx.send(f"Incorrect.\nIf you would like to try again type `{ctx.prefix}???`")
            else:
                await ctx.send("Correct!\n**Question 2: `How many letters are in the alphabet?`**\nType you answer below")
                try:
                    q2 = await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
                except asyncio.TimeoutError:
                    await ctx.send('Timeout Error')
                else: 
                    if q2.content != "26":
                        await ctx.send(f"Incorrect.\nIf you would like to try again type `{ctx.prefix}???`")
                    else:
                        await ctx.send("Correct.\n**Question 3: `(Approx)How many stars are in the sky?`**\n**A)10 Million**\n**B) 100 Million**\n**C) 1,000 Million**\n**D) 100,000 Million**\nType you answer below [Format: A|B|C|D]")
                        try:
                            q3 = await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
                        except asyncio.TimeoutError:
                            await ctx.send('Timeout Error')
                        else: 
                            if q3.content != "D":
                                await ctx.send(f"Incorrect.\nIf you would like to try again type `{ctx.prefix}???`")
                            else:
                                await ctx.send(f"Correct!\nYou took {:.1000f} seconds!.format(duration))")
        
def setup(bot):
    bot.add_cog(other(bot))
