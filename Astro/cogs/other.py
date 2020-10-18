import discord

from discord import Embed
from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import context
from discord.ext.commands.cooldowns import BucketType

import time, datetime
from datetime import datetime

import os

import asyncio

import aiohttp

import random

import collections


class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def dice(self, ctx):
        dice = ['1', '2', '3', '4', '5', '6', 'off the table...\n*You Found The Mystery!*']
        embed = discord.Embed(title="Dice", description=f'The Dice Rolled {random.choice(dice)}', color=0x2F3136)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758138226874908705/766312838910181421/unknown.png")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,10,BucketType.user) 
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
          async with session.get('https://some-random-api.ml/joke') as resp:
            resp = await resp.json()
        await ctx.send(resp['joke'])
        
    @commands.command()
    @commands.cooldown(1,10,BucketType.user)
    async def binary(self, ctx, text: str):
        async with aiohttp.ClientSession() as session:
          async with session.get(f'https://some-random-api.ml/binary?text={text}') as resp:
            resp = await resp.json()
        await ctx.send(resp['binary'])
        
    @commands.command()
    @commands.cooldown(1,10,BucketType.user)
    async def text(self, ctx, text: str):
        async with aiohttp.ClientSession() as session:
          async with session.get(f'https://some-random-api.ml/binary?decode={text}') as resp:
            resp = await resp.json()
        await ctx.send(resp['binary'])
        
    @commands.command()
    @commands.cooldown(1,10,BucketType.user) 
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
          async with session.get('https://some-random-api.ml/meme') as resp:
            resp = await resp.json()
        embed = discord.Embed(title=resp['caption'], color=0x2F3136)
        embed.set_image(url=resp['image'])
        await ctx.send(embed=embed)

       
    @commands.command(aliases=['q'])
    @commands.cooldown(1,60,BucketType.user) 
    async def quiz(self, ctx):
        qa = {
            "`What was Halloween originally called?`": "HALLOWS EVE",
            "`What was candy corn originally called?`": "CHICKEN FEED",
            "`(Approx)How much money does the average American spend on Halloween every year?`\n**A) $45\nB) $60\nC) $85\nD) $100**": "C"
        }
        total_questions = len(qa)
        start_time = time.time()

        def check(message):
            return ctx.author == message.author and ctx.channel == message.channel

        for i, (question, answer) in enumerate(qa.items()):
            content = ""
            append = "Type your answer below"

            if i == 0:
                content += "Quest Started!\n"
            elif i == 2:
                append += " [Format: A|B|C|D]"
            else:
                content += "Correct!\n"
            content += (f"**Question {i+1})** {question}\n"
                        f"{append}")
            await ctx.send(content)

            try:
                message = await self.bot.wait_for("message", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Timeout Error")

            if message.content.upper() != answer:
                return await ctx.send(f"Incorrect.\nIf you would like to try again type `{ctx.prefix}quest`")
        time_taken = time.time()- start_time
        await ctx.send(f"Correct!\nYou took **{time_taken:,.2f} seconds!**")


def setup(bot):
    bot.add_cog(other(bot))
