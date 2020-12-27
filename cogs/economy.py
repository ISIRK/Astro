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

from random import randint
import discord
from discord.ext import commands
import random, json
from discord.ext.commands.cooldowns import BucketType

tools = "tools/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class Jobs:
    
    def beg(self, balance):
        money = random.randint()


class economy(commands.Cog):
    '''Economy Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.jobs = Jobs()
    
    @commands.command()
    @commands.guild_only()
    async def register(self, ctx):
        """Registers a bank account bound to the guild with $50"""
        s = await self.bot.db.fetchrow("SELECT * FROM economy WHERE userId = $1 and guildId = $2", ctx.author.id, ctx.guild.id)
        if s:
            return await ctx.send(embed = discord.Embed(description = "You already have an account!", color=color))
        elif not s:
            await self.bot.db.execute("INSERT INTO economy(userId, guildId, cashBalance) VALUES($1, $2, $3)", ctx.author.id, ctx.guild.id, 50)
            await ctx.send(embed = discord.Embed(description = "Bank account register succesful, to remove your account run: `delete`", color=color))
    
    @commands.command(name = "delete")
    @commands.guild_only()
    async def delete_account(self, ctx):
        """Closes your account in this guild"""
        s = await self.bot.db.fetchrow("SELECT * FROM economy WHERE userId = $1 and guildId = $2", ctx.author.id, ctx.guild.id)
        if s:
            await self.bot.db.execute("DELETE FROM economy WHERE userId = $1 AND guildId = $2", ctx.author.id, ctx.guild.id)
            await ctx.send(embed = discord.Embed(description = "Successfully closed your bank account for this guild.", color=color))
        if not s:
            return await ctx.send(embed = discord.Embed(description = "You don't have an account!", color=color))
    
    @commands.command(aliases = ["bal"])
    async def balance(self, ctx, user: discord.Member = None):
        '''See the balance of yourself or the mentioned user'''
        if not user: user = ctx.author
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE guildid = $1 and userid = $2", ctx.guild.id, user.id)
        if not s: return await ctx.send("That user doesn't have a bank account!")
        bank, cash = s['bankbalance'], s['cashbalance']
        if not bank: bank = 0
        if not cash: cash = 0
        embed = discord.Embed(
            title = f"{str(user)}'s balance:",
            description = f"Bank: ${bank}\nCash: ${cash}",
            color = color
        )
        await ctx.send(embed = embed)

    @commands.cooldown(1,120,BucketType.user)
    @commands.command()
    async def work(self, ctx):
        '''Work and get a random amount of money inbetween $1 and $100'''
        try:
            s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE guildid = $1 and userid = $2", ctx.guild.id, ctx.author.id)
            bal = s['cashbalance']
            pay = random.randint(1, 100)
            total = bal+pay
            await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE guildId = $2 and userId = $3", total, ctx.guild.id, ctx.author.id)
            await ctx.send(f'You worked and gained ${pay}!')
        except Exception as e:
            return await ctx.send(f"User does not have a bank account.")
        
    ''' WIP
    @commands.command()
    async def deposit(self, ctx):
        try:
            s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE guildid = $1 and userid = $2", ctx.guild.id, ctx.author.id)
            bal = s['cashbalance']
            cash = 0
            await self.bot.db.execute("UPDATE economy SET cashbalance = $1 and bankbalance = $2 WHERE guildId = $3 and userId = $4", cash, bal, ctx.guild.id, ctx.author.id)
            await ctx.send(f'Deposited {bal} into the bank.')
        except Exception as e:
            return await ctx.send(f"{e}") #User does not have a bank account.
    '''

def setup(bot):
    bot.add_cog(economy(bot))
