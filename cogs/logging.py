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

off = "<:xon:792824364658720808><:coff:792824364483477514>"
on = "<:xoff:792824364545605683><:con:792824364558843956>"

class logging(commands.Cog):
    '''Logging Commands'''
    def __init__(self, bot):
        self.bot = bot
            
    # Listeners
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.bot.db.execute("INSERT INTO guilds (guildId, logging) VALUES($1, $2)", guild.id, False)

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
            timestamp=datetime.datetime.utcnow(),
            color=color
        )
        await c.send(embed=embed)
        
    @commands.Cog.listener('on_guild_remove')
    async def on_guild_leave(self, guild):

        await self.bot.db.execute("DELETE FROM guilds WHERE guildID = $1", guild.id)

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
            timestamp=datetime.datetime.utcnow(),
            color=color
        )
        await c.send(embed=embed)
        
    # Commands
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def settings(self, ctx):
        '''See the toggleable guild settings.'''
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", ctx.guild.id)
        error = discord.Embed(title="⚠️ Error", description="There was a problem with getting your guilds data.\nThis means that your guild is not in my database.\nPlease [re-invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot) and run this command again.", color=color)
        if not s: return await ctx.send(embed=error)
        logging, channel = s['logging'], s['channel']

        if logging is True:
            emoji = on
        else:
            emoji = off
        
        if channel is None:
            c = "No Channel Set"
        else:
            c = channel

        embed = discord.Embed(title=f"{ctx.guild} Settings",
                              description=f"Logging: {emoji}\n> Channel: `{c}`",
                              color=color
                             )
        await ctx.send(embed=embed)
    
    @commands.is_owner()
    @commands.command()
    async def toggle(self, ctx):
        await self.bot.db.execute("UPDATE guilds SET logging = $1 WHERE guildId = $2 ", True, ctx.guild.id)
        await ctx.send('Toggled!')
        
def setup(bot):
    bot.add_cog(logging(bot))
