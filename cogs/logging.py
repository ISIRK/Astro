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

import discord
from discord.ext import commands
import json, datetime
from discord.ext.commands.cooldowns import BucketType

tools = "tools/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class logging(commands.Cog):
    '''Logging Commands'''
    def __init__(self, bot):
        self.bot = bot
            
    # Listeners
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        x = datetime.datetime.utcnow()
        c = self.bot.get_channel(792869360925671444)
        embed = discord.Embed(
            title="Guild Joined!",
            description=("```yaml\n"
                         f"Guild Name - {guild}\n"
                         f"Guild ID - {guild.id}\n"
                         f"Guild Owner - {guild.owner} [{guild.owner.id}]\n"
                         f"Guild Created - {guild.created_at.strftime('%b %d, %Y %I:%M %p')}\n"
                         f"Guild Members - {len(guild.members)}\n"
                         "```"
                         ),
            timestamp=x.strftime("%b %d %Y %H:%M:%S"),
            color=color
        )
        await c.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild):
        x = datetime.datetime.utcnow()
        c = self.bot.get_channel(792869360925671444)
        embed = discord.Embed(
            title="Guild Left!",
            description=("```yaml\n"
                         f"Guild Name - {guild}\n"
                         f"Guild ID - {guild.id}\n"
                         f"Guild Owner - {guild.owner} [{guild.owner.id}]\n"
                         f"Guild Created - {guild.created_at.strftime('%b %d, %Y %I:%M %p')}\n"
                         f"Guild Members - {len(guild.members)}\n"
                         "```"
                         ),
            timestamp=x.strftime("%b %d %Y %H:%M:%S"),
            color=color
        )
        await c.send(embed=embed)
        
    # Commands
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def settings(self, ctx):
        await ctx.send('Comming Soon!')
        
def setup(bot):
    bot.add_cog(logging(bot))
