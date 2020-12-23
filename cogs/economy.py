from random import randint
import discord
from discord.ext import commands
import random, json

tools = "tools/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class Jobs:
    
    def beg(self, balance):
        money = random.randint()


class economy(commands.Cog):
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

    ''' WIP
    @commands.command()
    async def work(self, ctx):
        cash 
        await self.bot.db.execute("")
    '''

        

    

def setup(bot):
    bot.add_cog(economy(bot))
