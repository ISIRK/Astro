import discord
import subprocess as sp
from discord.ext import commands

class test(commands.Cog(hidden=True)):
    '''Testing Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, title, *options):
        reactions = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"}
        s = ""
        num = 1
        for i in options: 
            s += f"{num} - {i}\n" 
            num += 1
        msg = await ctx.send(embed = discord.Embed(title = title, descrioption = s, color=color))
        for i in range(1, len(options) + 1): await msg.add_reaction(reactions[i])

        
def setup(bot):
    bot.add_cog(test(bot))
