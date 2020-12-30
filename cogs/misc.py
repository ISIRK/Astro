'''

MIT License

Copyright (c) 2020 isirk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import discord, os, io, datetime, time, json, asyncio, aiohttp, random, collections, mystbin
from discord import Spotify
from discord.user import User
from discord.utils import get
from jishaku import codeblocks
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import context
from discord.ext.commands.cooldowns import BucketType

tools = "tools/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class misc(commands.Cog):
    '''Miscellaneous Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.myst = mystbin.Client()
        
        
    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    async def joke(self, ctx):
        '''Get a joke'''
        async with self.session.get("https://dadjoke-api.herokuapp.com/api/v1/dadjoke") as r:
            resp = await r.json()
        await ctx.send(resp['joke'])
        
    @commands.command()
    async def translate(self, ctx, *, message):
        '''Translate text to english.'''
        async with self.session.get(f"http://bruhapi.xyz/translate/{message}") as r:
            resp = await r.json()
        embed = discord.Embed(title="Translate", description=f"Original: {resp['original']}\nTranslation: {resp['text']}", color=color)
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def binary(self, ctx, *, text: str):
        '''Change text into binary'''
        if len(text) > 25:
            await ctx.send(f"{ctx.author}'s dick is too long")
        else:
            async with self.session.get(f'https://some-random-api.ml/binary?text={text}') as resp:
                resp = await resp.json()
            await ctx.send(resp['binary'])
        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def text(self, ctx, *, binary: str):
        '''Change binary into text'''
        async with self.session.get(f'https://some-random-api.ml/binary?decode={binary}') as resp:
            resp = await resp.json()
        await ctx.send(resp['text'])
        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user) 
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
    @commands.cooldown(1,3,BucketType.user) 
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

    @commands.cooldown(1,10,BucketType.user)
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
                    embed.add_field(name='Weather', value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}°\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}°\n**🌡️ Daily High:** {weather_response['main']['temp_max']}°\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}°\n**<:humidity:727253612778094683> Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph", inline=False)
                    embed.add_field(name='Time', value=f"**🕓 Local Time:** {localTime.strftime('%I:%M %p')}\n **🌅 Sunrise Time:** {sunriseTime.strftime('%I:%M %p')}\n **🌇 Sunset Time:** {sunsetTime.strftime('%I:%M %p')}")
                    embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    embed.set_footer(text=footer, icon_url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def replace(self, ctx, char, *, text):
      '''Send a message with an emoji in between each word'''
      await ctx.send(text.replace(" ", f" {char} "))

    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def poll(self, ctx, title, *options):
        '''Make a quick poll'''
        reactions = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"}
        s = ""
        num = 1
        for i in options: 
            s += f"{num} - {i}\n" 
            num += 1
        embed = discord.Embed(title = title, description = s, color=color)
        embed.set_footer(text=footer)
        try:
            await ctx.channel.purge(limit=1)
        except:
            pass
        msg = await ctx.send(embed=embed)
        for i in range(1, len(options) + 1): await msg.add_reaction(reactions[i])

    @commands.command(aliases = ["myst", "paste"])
    @commands.cooldown(1,3,BucketType.user)
    async def mystbin(self, ctx, *, code):
        """Post code to mystbin."""
        code = codeblocks.codeblock_converter(code)
        language = ""
        if code[0]: language = code[0]
        elif not code[0]: language = "txt"
        url = await self.myst.post(code[1], syntax = language)
        await ctx.send(f"{ctx.author.mention} Here is your code <:join:736719688956117043> {str(url)}")
           
    '''                          
    @commands.command()
    async def spotify(self, ctx, user: discord.Member = None):
        # Returns info about spotify playback.
        if user == None:
            user = ctx.author
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(
                        title = f"{user.name}'s Spotify",
                        description = "Listening to {}".format(activity.title),
                        color = activity.color)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.add_field(name="Duration", value=activity.duration, inline=False)
                    embed.add_field(name="Elapsed", value="{}".format(activity.created_at.strftime("%H:%M")))
                    embed.set_footer(text=footer)
                    return await ctx.send(embed=embed)
            return await ctx.send('No Spotify Activity Found')
        return await ctx.send('User is not playing anything.')
    '''

def setup(bot):
    bot.add_cog(misc(bot))
