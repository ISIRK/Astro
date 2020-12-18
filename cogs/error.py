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

import discord, json, datetime
from discord.ext.commands import Cog
from discord.ext import commands

tools = "tools/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class ErrorHandler(Cog):
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
        elif isinstance(error, discord.NotFound): await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.CommandOnCooldown): await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.MaxConcurrencyReached): await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
        elif isinstance(error, commands.CheckFailure): await ctx.reply(embed = discord.Embed(title = str(error), color = discord.Color.red()))
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
    bot.add_cog(ErrorHandler(bot))
