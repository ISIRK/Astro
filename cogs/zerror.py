import discord
from discord.ext import commands
from discord.ext.commands import Cog
import datetime

class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed = discord.Embed(title = "Command Not Found.", description= f"Use `{ctx.prefix}help for a list of commands", color = discord.Color.red())) #return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.NotOwner):
            await ctx.send(embed = discord.Embed(title = "You are not an owner.", color = discord.Color.red())) #return
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, discord.NotFound): await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.CommandOnCooldown): await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        else:
            embed = discord.Embed(
                title = "An error occurred!",
                description = f"Reported to the support server. Need more help? [Join the support server](https://discord.gg/7yZqHfG)\n```Error: \n{str(error)}```",
                timestamp = datetime.datetime.utcnow(),
                color = discord.Color.red()
            )
            embed.set_footer(text = f"Caused by: {ctx.command}")
            await ctx.send(embed = embed)

            #Support server embed
            embed = discord.Embed(
                title = f"An error occured!",
                description = f"```{str(error)}```",
                timestamp = datetime.datetime.utcnow(),
                color = discord.Color.red()
            )
            c = self.bot.get_channel(783138336323403826) 
            embed.add_field(
                name = "Details:",
                value = f"""
                Caused by: `{str(ctx.author)} [{ctx.author.id}]`
                In guild: `{str(ctx.guild)} [{ctx.guild.id}]`
                Command: `{ctx.command}`
                """
            )
            await c.send(embed = embed)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
