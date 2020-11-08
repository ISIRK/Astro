import discord

from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import context
from discord.ext.commands.cooldowns import BucketType

import time, datetime
from datetime import datetime

import os

import io

import json

import asyncio

import aiohttp

import random

import collections

colorfile = "/home/pi/Discord/Sirk/utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)


class other(commands.Cog):
    '''Random Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def dice(self, ctx):
        '''Roll a dice'''
        dice = ['1', '2', '3', '4', '5', '6', 'off the table...\n*You Found The Mystery!*']
        embed = discord.Embed(title="Dice", description=f'The Dice Rolled {random.choice(dice)}', color=color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758138226874908705/766312838910181421/unknown.png")
        await ctx.send(embed=embed)

        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def joke(self, ctx):
        '''Get a joke'''
        async with self.session.get("https://dadjoke-api.herokuapp.com/api/v1/dadjoke") as r:
            resp = await r.json()
        await ctx.send(resp['joke'])
        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def binary(self, ctx, *, text: str):
        '''Change text into binary'''
        if "@everyone" in text:
            await ctx.send('Please refrain from using `@everyone`.')
        elif "@here" in text:
            await ctx.send('Please refrain from using `@here`.')
        else:
            async with self.session.get(f'https://some-random-api.ml/binary?text={text}') as resp:
                resp = await resp.json()
            await ctx.send(resp['binary'])
        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def text(self, ctx, *, binary: str):
        '''Change binary into text'''
        if "010000000110010101110110011001010111001001111001011011110110111001100101" in binary:
            await ctx.send('Please refrain from using `@everyone`.')
        elif "0100000001101000011001010111001001100101" in binary:
            await ctx.send('Please refrain from using `@here`.')
        else:
            async with session.get(f'https://some-random-api.ml/binary?decode={binary}') as resp:
                resp = await resp.json()
            await ctx.send(resp['text'])
        
    @commands.command()
    @commands.cooldown(1,5,BucketType.user) 
    async def meme(self, ctx):
        '''Get a random meme'''
        async with session.get('https://meme-api.herokuapp.com/gimme/dankmemes') as resp:
            resp = await resp.json()
            
        if resp['nsfw'] == True and not ctx.channel.is_nsfw():
            return await ctx.send("⚠️ This meme is marked as NSFW and I can't post it in a non-nsfw channel.")
        else:
            embed = discord.Embed(title=resp['title'], url=resp['postLink'], color=color)
            embed.set_image(url=resp['url'])
            embed.set_footer(text="r/Dankmemes")
            await ctx.send(embed=embed)

    @commands.command(aliases=['ph'])
    @commands.cooldown(1,5,BucketType.user) 
    async def programmerhumor(self, ctx):
        '''Get a programmer humor meme'''
        async with session.get('https://meme-api.herokuapp.com/gimme/ProgrammerHumor') as resp:
            resp = await resp.json()
        embed = discord.Embed(title=resp['title'], url=resp['postLink'], color=color)
        embed.set_image(url=resp['url'])
        embed.set_footer(text="r/ProgrammerHumor")
        await ctx.send(embed=embed)

    @commands.command(aliases=['mc'])
    @commands.cooldown(1,3,BucketType.user)
    async def minecraft(self, ctx, *, username):
        '''Get a minecraft users stats'''
        async with session.get(f'https://api.mojang.com/users/profiles/minecraft/{username}?at=') as resp:
            resp = await resp.json()
        embed=discord.Embed(title=f"Stats for {resp['name']}", description=f"ID: `{resp['id']}`", color=color)
        embed.set_thumbnail(url=f"https://minotar.net/helm/{username}/100.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['mcs'])
    @commands.cooldown(1,3,BucketType.user)
    async def minecraftserver(self, ctx, *, server):
        '''Get a minecraft servers stats'''
        async with session.get(f'http://mcapi.xdefcon.com/server/{server}/full/json') as resp:
            resp = await resp.json()
                            
        embed=discord.Embed(title=f"Stats for {server}", description=f"IP: {resp['serverip']}\nStatus: {resp['serverStatus']}\nPing: {resp['ping']}\nVersion: {resp['version']}\nPlayers: {resp['players']}\nMax Players: {resp['maxplayers']}", color=color)
        embed.set_thumbnail(url=f"https://api.minetools.eu/favicon/{server}/25565")
        await ctx.send(embed=embed)

            
    @commands.command(aliases=['q'])
    @commands.cooldown(1,60,BucketType.user) 
    async def quiz(self, ctx):
        '''Take a halloween quiz'''
        qa = {
            "`What was Halloween originally called?`": "ALL HALLOWS EVE",
            "`What was candy corn originally called?`": "CHICKEN FEED",
            "`(Approx)How much money does the average American spend on Halloween every year?`\n**A) $45\nB) $60\nC) $85\nD) $100**": "C",
            "`(Approx)What percentage of kids like to recieve gum for halloween?`": "10",
            "`When is Halloween?`": "OCTOBER 31",
            "`What country was Trick-or-treating first done?`": "CANADA"
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
                message = await self.bot.wait_for("message", timeout=45.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Timeout Error")

            if message.content.upper() != answer:
                return await ctx.send(f"Incorrect.\nIf you would like to try again type `{ctx.prefix}quest`")
        time_taken = time.time()- start_time
        await ctx.send(f"Correct!\nYou took **{time_taken:,.2f} seconds!**")



def setup(bot):
    bot.add_cog(other(bot))
