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
        """Registers a bank account with $50"""
        s = await self.bot.db.fetchrow("SELECT * FROM economy WHERE userId = $1", ctx.author.id)
        if s:
            return await ctx.send(embed = discord.Embed(description = "You already have an account!", color=self.bot.color))
        elif not s:
            await self.bot.db.execute("INSERT INTO economy(userId, cashBalance, bankBalance) VALUES($1, $2, $3)", ctx.author.id, 50, 0)
            await ctx.send(embed = discord.Embed(description = "Bank account register succesful, to remove your account run: `delete`", color=self.bot.color))
    
    @commands.command(name = "delete")
    @commands.guild_only()
    async def delete_account(self, ctx):
        """Closes your account"""
        s = await self.bot.db.fetchrow("SELECT * FROM economy WHERE userId = $1", ctx.author.id)
        if s:
            await self.bot.db.execute("DELETE FROM economy WHERE userId = $1", ctx.author.id)
            await ctx.send(embed = discord.Embed(description = "Successfully closed your bank account.", color=self.bot.color))
        if not s:
            return await ctx.send(embed = discord.Embed(description = "You don't have an account!", color=self.bot.color))
    
    @commands.command(aliases = ["bal"])
    async def balance(self, ctx, user: discord.Member = None):
        '''See the balance of yourself or the mentioned user'''
        if not user: user = ctx.author
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", user.id)
        if not s: return await ctx.send("That user doesn't have a bank account!")
        bank, cash = s['bankbalance'], s['cashbalance']
        if not bank: bank = 0
        if not cash: cash = 0
        embed = discord.Embed(
            title = f"{str(user.name)}'s balance:",
            description = f"💰 Cash: ${cash}\n🏦 Bank: ${bank}",
            color = self.bot.color
        )
        await ctx.send(embed = embed)

    @commands.cooldown(1,120,BucketType.user)
    @commands.command()
    async def work(self, ctx):
        '''Work and get a random amount of money in between $1 and $100'''
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not s:
            await ctx.send("That user doesn't have a bank account!")
            #ctx.command.reset_cooldown(ctx)
        bal = s['cashbalance']
        pay = random.randint(1, 100)
        total = bal+pay
        await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", total, ctx.author.id)
        await ctx.send(f'You worked and gained ${pay}!')

    @commands.cooldown(1,60,BucketType.user)
    @commands.command()
    async def rob(self, ctx, * user: discord.Member):
        '''
        Rob another user
        '''
        user = ctx.guild.get_member(user)
        a = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not a:
            await ctx.send("You don't have a bank account!")
        u = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", user.id)
        if not u:
            await ctx.send("That user doesn't have a bank account!")
        
        c = random.choice(100, 200)
        
        if u['cashbalance'] < c:
            await ctx.send(f"<:PepePoint:759934591590203423> {user} doesn't have enough money. Try robbing someone with more money.")
        try:
            await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", a['cashbalance']-c, user.id)
            await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", u['cashbalance']+c, ctx.author.id)
            await ctx.send(f'You stole ${c} from **{user.name}**')
        except Exception as e:
            await ctx.send(f'```py\n{e}```')
        
    @commands.cooldown(1,3,BucketType.user)
    @commands.command(aliases=['dep'])
    async def deposit(self, ctx):
        '''Deposit all of your money into the bank.'''
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not s: return await ctx.send("That user doesn't have a bank account!")
        cash = s['cashbalance']
        if cash == 0:
            await ctx.send('No Money in your wallet.')
        else:
            await self.bot.db.execute("UPDATE economy SET cashbalance = 0, bankbalance = cashbalance+bankbalance WHERE userId = $1", ctx.author.id)
            await ctx.send(f"Deposited ${cash} into the bank.")
    
    @commands.cooldown(1, 43200, BucketType.user)
    @commands.command()
    async def daily(self, ctx):
        '''Get daily coins.'''
        s = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", ctx.author.id)
        if not s: return await ctx.send("That user doesn't have a bank account!")
        await self.bot.db.execute("UPDATE economy SET cashbalance = cashbalance+1000 WHERE userId = $1", ctx.author.id)
        await ctx.send("Collected **1,000** daily coins!")

    @commands.cooldown(1,3,BucketType.user)
    @commands.group(brief="Main commands")
    async def shop(self, ctx):
        '''A shop to buy things with your coins. WIP'''
        
        embed = discord.Embed(title=f"{ctx.guild.name}'s Shop", description="This command is a work in progress.", color=self.bot.color)
        embed.add_field(name="Multiplier", value="💰 Multiply your earnings for the command `work`!\nCost: **$1,000**", inline=False)
        embed.add_field(name="SubCommands", value="`shop` - This Command", inline=False)
        embed.set_footer(text=self.bot.footer)
        embed.set_author(name="Shop", icon_url=ctx.guild.icon_url)

        if ctx.invoked_subcommand is None:
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(economy(bot))
