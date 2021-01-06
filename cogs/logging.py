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
import json, datetime, asyncio, datetime
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
        
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(
                guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            if to_send.permissions_for(guild.me).embed_links:  # We can embed!
                e = discord.Embed(
                    color=color, title="Thanks for Adding Me!")
                e.description = f"Thank you for adding me to this server!"
                e.add_field(name="Startup", value="To get started type `^help`", inline=False)
                e.add_field(name="Logging", value="If you are a sever admin/moderator get the mod-log setup with `^help logging`", inline=False)
                e.add_field(name="Support", value="If you have any questions feel free to ask in our [support server](https://discord.gg/7yZqHfG)", inline=False)
                e.set_thumbnail(url='https://asksirk.com/img/sirk-christmas.jpg')
                try:
                    await to_send.send(embed=e)
                except:
                    pass
            else:  # We were invited without embed perms...
                msg = f"Thank you for adding me to this server!\nTo get started type `^help`\nIf you are a sever admin/moderator get the mod-log setup with `^help logging`\nIf you have any questions feel free to ask in our support server. (https://discord.gg/7yZqHfG)"
                try:
                    await to_send.send(msg)
                except:
                    pass
        
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
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        print(guild)
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", guild.id)
        channel = s['channel']
        c = guild.get_channel(channel)
        
        value = [f"User: {member}(`{member.id}`)", f"Left: {datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')}", f"Current Members: {member.guild.member_count}"]
        
        if logging:
            if channel is not None:
                embed = discord.Embed(title=f"User Left!",
                                    description="\n".join(value),
                                    color=discord.Color.red()
                                    )
                embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
                embed.set_footer(text=footer)
                await c.send(embed=embed)
            else:
                pass
        else:
            pass
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", guild.id)
        logging, channel = s['logging'], s['channel']
        c = guild.get_channel(channel)
        
        value = [f"User: {member.mention} (`{member}`)", f"Joined: {member.joined_at.strftime('%B %d %Y - %H:%M:%S')}", f"Created: {member.created_at.strftime('%B %d %Y - %H:%M:%S')}", f"Current Members: {member.guild.member_count}"]
        
        if logging:
            if channel is not None:
                embed = discord.Embed(title=f"User Joined!",
                                    description='\n'.join(value),
                                    color=color
                                    )
                embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
                embed.set_footer(text=footer)
                await c.send(embed=embed)
            else:
                pass
        else:
            pass
        
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
            c = "`No Channel Set`"
        else:
            d = ctx.guild.get_channel(channel)
            c = d.mention

        embed = discord.Embed(title=f"{ctx.guild} Settings",
                              description=f"Logging: {emoji}\n> Channel: {c}",
                              color=color
                             )
        if logging:
            if channel is not None:
                embed.add_field(name="Currently Logging", value=" • Joins\n • Leaves\n • Kicks", inline=False)
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

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx):
        '''
        Remove the logging channel\n*Note: If this is removed, and logging is toggled on, it still will not log.*
        '''
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", ctx.guild.id)
        error = discord.Embed(title="⚠️ Error", description="There was a problem with getting your guilds data.\nThis means that your guild is not in my database.\nPlease [re-invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot) and run this command again.", color=color)
        if not s: return await ctx.send(embed=error)
        try:
            await self.bot.db.execute("UPDATE guilds SET channel = $1 WHERE guildId = $2 ", None, ctx.guild.id)
            await ctx.send(f'Removed your logging channel.')
        except Exception as e:
            return await ctx.send(f"Something went wrong, please try again.\n\nError:```py\n{e}```")
            
        
def setup(bot):
    bot.add_cog(logging(bot))
