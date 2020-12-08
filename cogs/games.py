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

import discord, random, json, time, asyncio, aiohttp
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

tools = "json/tools.json"
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
    
class games(commands.Cog):
    '''Game Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        
    @commands.cooldown(1,3,BucketType.user)   
    @commands.command(aliases=['cb'])
    async def chatbot(self, ctx, *, message):
        '''Talk to chatbot'''
        async with self.session.get(f"http://bruhapi.xyz/cb/{message}") as r:
            resp = await r.json()
        await ctx.send(resp['res'])
        
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
    async def quiz(self, ctx):
        '''Take a Chritmas quiz'''
        qa = {
            "`Was King William I of England was crowned on Christmas Day.(Yes/No)`": "YES",
            "`When is Christmas?`": "DECEMBER 25",
            "`Who delivers toys?`" : "SANTA"
        }
        total_questions = len(qa)
        start_time = time.time()

        def check(message):
            return ctx.author == message.author and ctx.channel == message.channel

        for i, (question, answer) in enumerate(qa.items()):
            content = ""
            append = "Type your answer below"

            if i == 0:
                content += "Quiz Started!\n"
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
                return await ctx.send(f"Incorrect.\nIf you would like to try again type `{ctx.prefix}quiz`")
        time_taken = time.time()- start_time
        await ctx.send(f"Correct!\nYou took **{time_taken:,.2f} seconds!**")

    
    @commands.cooldown(1,3,BucketType.user)
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

            await s.edit(embed= discord.Embed(title =result , description = f"I picked {botChoice} and you picked {reaction}.", color=color))

        except asyncio.TimeoutError: return await ctx.send("You didn't add a reaction in time!")

def setup(bot):
    bot.add_cog(games(bot))
