import discord

from discord.ext import commands

class test(commands.Cog):
    '''Testing Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, title, *options):
        reactions = {1: "\U00000031", 2: "\U00000032", 3: "\U00000033", 4: "\U00000034", 5: "\U00000035", 6: "\U00000036", 7: "\U00000037", 8: "\U00000038", 9: "\U00000039", 10: "\U0001f51f"}
        s = ""
        num = 1
        for i in options: 
            s += f"{num} - {i}\n" 
            num += 1
        msg = await ctx.send(embed = discord.Embed(title = title, descrioption = s))
        for i in range(1, len(options) + 1): await msg.add_reaction(reactions[i])

        
def setup(bot):
    bot.add_cog(test(bot))
