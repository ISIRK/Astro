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
import json, datetime, asyncio
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
    
    # Guild Events
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
        
    # Moderation Events
    @commands.Cog.listener('on_memeber_remove')
    async def on_kick(self, guild, user):
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", ctx.guild.id)
        channel = s['channel']
        c = self.bot.get_channel(channel)

        if guild.me.guild_permissions.view_audit_log:
            log = await guild.audit_logs(limit=1).flatten()
            log = log[0]
            if log.action is discord.AuditLogAction.ban:
                mod = log.user
                returnList.append(f"Moderator: {mod} [{mod.id}]")
                returnList.append(f"Reason: \n ```{log.reason}```")
        try:
            embed = discord.Embed(title="User Banned!",
                                      description="\n".join(returnList))
            await c.send(embed=embed)
        except discord.Forbidden:
            return
        
    # Commands    
    @commands.command(aliases=['set'])
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
            d = ctx.guild.get_channel(channel)
            c = d.mention

        embed = discord.Embed(title=f"{ctx.guild} Settings",
                              description=f"Logging: {emoji}\n> Channel: {c}",
                              color=color
                             )
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def toggle(self, ctx):
        '''
        Toggle Logging\n*Note: You need to set a channel before it starts logging.*
        '''
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", ctx.guild.id)
        error = discord.Embed(title="⚠️ Error", description="There was a problem with getting your guilds data.\nThis means that your guild is not in my database.\nPlease [re-invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot) and run this command again.", color=color)
        if not s: return await ctx.send(embed=error)
        log = s['logging']
        if log:
            await self.bot.db.execute("UPDATE guilds SET logging = $1 WHERE guildId = $2 ", False, ctx.guild.id)
            await ctx.send(f'{off} | Logging Toggled Off!')
        elif not log:
            await self.bot.db.execute("UPDATE guilds SET logging = $1 WHERE guildId = $2 ", True, ctx.guild.id)
            await ctx.send(f'{on} | Logging Toggled On!')
            
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        '''
        Set the logging channel\n*Note: You need to toggle logging before it starts logging.*
        '''
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", ctx.guild.id)
        error = discord.Embed(title="⚠️ Error", description="There was a problem with getting your guilds data.\nThis means that your guild is not in my database.\nPlease [re-invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot) and run this command again.", color=color)
        if not s: return await ctx.send(embed=error)
        log = channel.id
        try:
            await self.bot.db.execute("UPDATE guilds SET channel = $1 WHERE guildId = $2 ", log, ctx.guild.id)
            await ctx.send(f'Set {channel.mention} to be the mod-log channel.')
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
        c = ctx.guild.get_channel(log)
        try:
            await c.send(f'{channel.mention} --> {log}')
        except Exception as e:
            return await ctx.send(f"I do not have permissions to send in {c}\nPlease change my permissions and try again.")
        
def setup(bot):
    bot.add_cog(logging(bot))
