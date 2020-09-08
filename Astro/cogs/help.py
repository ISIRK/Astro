import discord
from discord import Embed
from discord.ext import commands

@commands.command(pass_context=True)
@commands.has_permissions(add_reactions=True,embed_links=True)
async def help(self,ctx,*cog):
    """Gets all cogs and commands of mine."""
    try:
            """Helps me remind you if you pass too many args."""
            if len(cog) > 1:
                halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Color.red())
                await ctx.message.author.send('',embed=halp)
            else:
                """Command listing within a cog."""
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__)
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    halp.add_field(name=c.name,value=c.help,inline=False)
                            found = True
                if not found:
                    """Reminds you if that cog doesn't exist."""
                    halp = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=discord.Color.red())
                else:
                    await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('',embed=halp)
    except:
        await ctx.send("Excuse me, I can't send embeds.")
        
def setup(bot):
    bot.add_command(help)