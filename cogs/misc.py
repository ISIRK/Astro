import discord

from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import context
from discord.ext.commands.cooldowns import BucketType

import os

import io

import datetime

import time

import json

import asyncio

import aiohttp

import random

import collections


tools = "/home/pi/Discord/Sirk/utils/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

def rps_winner(userOneChoice, userTwoChoice):
    if userOneChoice == "\U0001faa8":
        if userTwoChoice == "\U00002702": return "You won!"
        if userTwoChoice == "\U0001faa8": return "Tie!"
        if userTwoChoice == "\U0001f4f0": return "I won!"
    elif userOneChoice == "\U00002702":
        if userTwoChoice == "\U00002702": return "Tie!"
        if userTwoChoice == "\U0001faa8": return "I won!"
        if userTwoChoice == "\U0001f4f0": return "You Won!"
    elif userOneChoice == "\U0001f4f0":
        if userTwoChoice == "\U00002702": return "I won!"
        if userTwoChoice == "\U0001faa8": return "You won!"
        if userTwoChoice == "\U0001f4f0": return "Tie!"
    else: return "error"


class misc(commands.Cog):
    '''Miscellaneous Commands'''
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
        embed.set_footer(text=footer)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def joke(self, ctx):
        '''Get a joke'''
        async with self.session.get("https://dadjoke-api.herokuapp.com/api/v1/dadjoke") as r:
            resp = await r.json()
        await ctx.send(resp['joke'])
     
    @commands.command(aliases=['cb'])
    @commands.cooldown(1,3,BucketType.user)
    async def chatbot(self, ctx, *, message):
        '''Talk to chatbot'''
        async with self.session.get(f"http://bruhapi.xyz/cb/{message}") as r:
            resp = await r.json()
        await ctx.send(resp['res'])
        
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
            async with self.session.get(f'https://some-random-api.ml/binary?decode={binary}') as resp:
                resp = await resp.json()
            await ctx.send(resp['text'])
        
    @commands.command()
    @commands.cooldown(1,5,BucketType.user) 
    async def meme(self, ctx):
        '''Get a random meme'''
        async with self.session.get('https://meme-api.herokuapp.com/gimme/dankmemes') as resp:
            resp = await resp.json()
            
        if resp['nsfw'] == True and not ctx.channel.is_nsfw():
            return await ctx.send("⚠️ This meme is marked as NSFW and I can't post it in a non-nsfw channel.")
        else:
            embed = discord.Embed(title=resp['title'], url=resp['postLink'], color=color)
            embed.set_image(url=resp['url'])
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"r/Dankmemes | {footer}")
            await ctx.send(embed=embed)

    @commands.command(aliases=['ph'])
    @commands.cooldown(1,5,BucketType.user) 
    async def programmerhumor(self, ctx):
        '''Get a programmer humor meme'''
        async with self.session.get('https://meme-api.herokuapp.com/gimme/ProgrammerHumor') as resp:
            resp = await resp.json()
        embed = discord.Embed(title=resp['title'], url=resp['postLink'], color=color)
        embed.set_image(url=resp['url'])
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"r/ProgrammerHumor | {footer}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['mc'])
    @commands.cooldown(1,3,BucketType.user)
    async def minecraft(self, ctx, *, username):
        '''Get a minecraft users stats'''
        async with self.session.get(f'https://api.mojang.com/users/profiles/minecraft/{username}?at=') as resp:
            resp = await resp.json()
        embed=discord.Embed(title=f"Stats for {resp['name']}", description=f"ID: `{resp['id']}`", color=color)
        embed.set_image(url=f"https://minotar.net/armor/body/{username}/100.png")
        embed.set_thumbnail(url=f"https://minotar.net/helm/{username}/100.png")
        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{username}/100.png")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command(aliases=['mcs'])
    @commands.cooldown(1,3,BucketType.user)
    async def minecraftserver(self, ctx, *, server):
        '''Get a minecraft servers stats'''
        async with self.session.get(f'http://mcapi.xdefcon.com/server/{server}/full/json') as resp:
            resp = await resp.json()
                            
        embed=discord.Embed(title=f"Stats for {server}", description=f"IP: {resp['serverip']}\nStatus: {resp['serverStatus']}\nPing: {resp['ping']}\nVersion: {resp['version']}\nPlayers: {resp['players']}\nMax Players: {resp['maxplayers']}", color=color)
        embed.set_thumbnail(url=f"https://api.minetools.eu/favicon/{server}/25565")
        embed.set_footer(text=footer)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

            
    @commands.command()
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

    @commands.cooldown(1,30,BucketType.user)
    @commands.command()
    async def weather(self, ctx, *, city_name:str):
        """Get the weather of a city/town by its name. State code is US only."""
        # Code By CraziiAce#0001
        async with aiohttp.ClientSession() as session:
            url = "http://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=168ced82a72953d81d018f75eec64aa0&units=imperial"
            async with session.get(url) as response:
                weather_response = await response.json()
                if weather_response['cod'] != 200:
                    await ctx.send(f"An error ocurred: `{weather_response['message']}`.")
                else:
                    currentUnix = time.time()
                    localSunrise = weather_response['sys']['sunrise'] + weather_response['timezone']
                    sunriseTime = datetime.datetime.utcfromtimestamp(localSunrise)
                    localSunset = weather_response['sys']['sunset'] + weather_response['timezone']
                    sunsetTime = datetime.datetime.utcfromtimestamp(localSunset)
                    localTimeUnix = currentUnix + weather_response['timezone']
                    localTime = datetime.datetime.utcfromtimestamp(localTimeUnix)
                    embed = discord.Embed(
                        title=f"Weather in {weather_response['name']}, {weather_response['sys']['country']}",
                        url = f"https://openweathermap.org/city/{weather_response['id']}",
                        description=weather_response['weather'][0]['description'],
                        color=color,
                    )
                    embed.add_field(name='Location:', value=f"**🏙️ City:** {weather_response['name']}\n**<:coordinates:727254888836235294> Longitude:** {weather_response['coord']['lon']}\n **<:coordinates:727254888836235294> Latitude:** {weather_response['coord']['lat']}", inline=False)
                    embed.add_field(name='Weather', value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}\n**🌡️ Daily High:** {weather_response['main']['temp_max']}\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}\n**<:humidity:727253612778094683> Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph", inline=False)
                    embed.add_field(name='Time', value=f"**🕓 Local Time:** {localTime.strftime('%I:%M %p')}\n **🌅 Sunrise Time:** {sunriseTime.strftime('%I:%M %p')}\n **🌇 Sunset Time:** {sunsetTime.strftime('%I:%M %p')}")
                    embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    embed.set_footer(text=footer, icon_url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)

    @commands.cooldown(1,10,BucketType.user)
    @commands.command()
    async def rps(self, ctx):
        """Rock paper scissors, either play against the bot or against a user"""
        choices = ["\U0001f4f0", "\U0001faa8", "\U00002702"]
        s = m = await ctx.send(embed = discord.Embed(title = f"Rock, Paper, Scissors.", description = f" {str(ctx.author)} Choose your weapon!", color=color))
        for i in choices:
            await m.add_reaction(i)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in choices

        try:
            reaction = await self.bot.wait_for('reaction_add', timeout = 30.0, check = check)
            reaction = reaction[0].emoji
            botChoice = random.choice(choices)
            result = rps_winner(reaction, botChoice)

            await s.edit(embed= discord.Embed(title = "Results:", description = f"I picked {botChoice} and you picked {reaction} \n\n{result}", color=color))

        except asyncio.TimeoutError: return await ctx.send("You didn't add a reaction in time!")

    @commands.command()
    async def replace(self, ctx, char, *, text):
      await ctx.send(text.replace(" ", f" {char} "))

def setup(bot):
    bot.add_cog(misc(bot))
