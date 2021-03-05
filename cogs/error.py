import discord, json, datetime, humanize
from discord.ext.commands import Cog
from discord.ext import commands

class error(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.NotOwner):
            await ctx.reply(embed = discord.Embed(title = f"Owner Only Command.", color = discord.Color.red())) #return # You are not an owner.
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, discord.NotFound):
            await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(embed = discord.Embed(title = f"You are on cooldown. Try again in {humanize.naturaldelta(datetime.timedelta(seconds=error.retry_after))}", color = discord.Color.red()))
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.reply(embed = discord.Embed(title = f"Command {ctx.command} is limited to `{error.number}` {'use' if error.number == 1 else 'uses'} per {error.per.name} at a time.", color = discord.Color.red()))
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.DisabledCommand):
            await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        else:
            embed = discord.Embed(
                title = "An error occurred!",
                description = f"Reported to the support server. Need more help? [Join the support server](https://discord.gg/7yZqHfG)\n```Error: \n{str(error)}```",
                timestamp = datetime.datetime.utcnow(),
                color = discord.Color.red()
            )
            embed.set_footer(text = f"Caused by: {ctx.command}")
            await ctx.reply(embed = embed)

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
    bot.add_cog(error(bot))
