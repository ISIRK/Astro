import discord
from discord.ext import commands
from discord.ext.commands import Cog
from datetime import datetime

class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored_errors = (commands.NotOwner) #commands.CommandNotFound, 
        
        error = getattr(error, "original", error)

        if isinstance(error, ignored_errors):
            return

        setattr(ctx, "original_author_id", getattr(ctx, "original_author_id", ctx.author.id))
        owner_reinvoke_errors = (
            commands.MissingAnyRole, commands.MissingPermissions,
            commands.MissingRole, commands.CommandOnCooldown, commands.DisabledCommand
        )

        if ctx.original_author_id in self.bot.owner_ids and isinstance(error, owner_reinvoke_errors):
            return await ctx.reinvoke()
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        #elif isinstance(error, commands.NotOwner):
            #await ctx.send(embed = discord.Embed(title = "You are not an owner.", color = discord.Color.red()))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, discord.NotFound): await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.CommandOnCooldown): await ctx.send(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        else:
            c = bot.get_channel(783138336323403826) 
            embed = discord.Embed(
                title = "An error occurred!",
                description = f"Reported to the support server. Need more help? [Join the support server](https://discord.gg/7yZqHfG)\n```Error: \n{str(error)}```",
                timestamp = datetime.datetime.utcnow()
            )
            embed.set_footer(text = f"Caused by: {ctx.command}")
            await ctx.send(embed = embed)

            #Support server embed
            embed = discord.Embed(
                title = f"An error occured!",
                description = f"```{str(error)}```",
                timestamp = datetime.datetime.utcnow()
            )
            embed.add_field(
                name = "Details:",
                value = f"""
                Caused by: `{str(ctx.author)} [{int(ctx.author)}]`
                In guild: `{str(ctx.guild)} [{int(ctx.guild)}]`
                Command: `{ctx.command}`
                """
            )
            await c.send(embed = embed)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
