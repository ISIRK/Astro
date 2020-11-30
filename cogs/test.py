import discord, os
import subprocess as sp
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

    @commands.command(aliases=['pull'], hidden = True)
    @commands.is_owner()
    async def sync(self, ctx):
        """Get the most recent changes from the GitHub repository
        Uses: p,sync"""
        embedvar = discord.Embed(title="Syncing...", description="Syncing with the GitHub repository and reloading the cogs, this should take up to 15 seconds", color=0xff0000, timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=embedvar)
        async with ctx.channel.typing():
            output = sp.getoutput('git pull')
        embedvar = discord.Embed(title="Synced", description="Sync with the GitHub repository has completed.\nAll cogs have been reloaded as well.", color=0x00ff00, timestamp=ctx.message.created_at)
        # Reload Cogs as well
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    return await ctx.send(f"```py\n{e}```")

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )
        
        await msg.edit(embed=embedvar)

        
def setup(bot):
    bot.add_cog(test(bot))
