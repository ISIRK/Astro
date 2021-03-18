import discord, json, datetime, asyncio, datetime
from discord.ext import commands

off = "<:off:801561937083105300>"
on = "<:on:801561937472520201>"

class config(commands.Cog):
    '''Configuration Commands'''
    def __init__(self, bot):
        self.bot = bot

    # Functions

    async def Logging_Check(self, guild):
        try:
            s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", guild)
            channel = s['channel']

            if channel:
                return channel
            else:
                return False
        except:
            return False

    async def Verify_Check(self, guild):
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", guild)
        vchannel, role = s['vchannel'], s['role']

        if vchannel and role is not None:
            return vchannel
        else:
            return False

            
    # Listeners
    
    # Guild Events
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.bot.db.execute("INSERT INTO guilds (guildId) VALUES($1)", guild.id)

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
            color=self.bot.color
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
                    color=self.bot.color, title="Thanks for Adding Me!")
                e.description = f"Thank you for adding me to this server!"
                e.add_field(name="Startup", value="To get started type `^help`", inline=False)
                e.add_field(name="Logging", value="If you are a sever admin/moderator get the mod-log setup with `^help logging`", inline=False)
                e.add_field(name="Verification", value="If you are a server admin make use `^help verify` to setup the react-to-verify process.", inline=False)
                e.add_field(name="Support", value="If you have any questions feel free to ask in our [support server](https://discord.gg/7yZqHfG)", inline=False)
                e.set_thumbnail(url=self.bot.user.avatar_url)
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
            color=self.bot.color
        )
        await c.send(embed=embed)
        
    # Moderation Events
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild

        e = await config.Logging_Check(self, guild.id)
        
        value = [f"User: {member}(`{member.id}`)", f"Left: {datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')}", f"Current Members: {member.guild.member_count}"]
        
        if e:
            embed = discord.Embed(title=f"User Left!",
                                description='\n'.join(value),
                                color=discord.Colour.red()
                                )
            embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
            embed.set_footer(text=self.bot.footer)
            c = self.bot.get_channel(e)
            await c.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild

        e = await config.Logging_Check(self, guild.id)
        
        value = [f"User: {member.mention} (`{member}`)", f"Joined: {member.joined_at.strftime('%B %d %Y - %H:%M:%S')}", f"Created: {member.created_at.strftime('%B %d %Y - %H:%M:%S')}", f"Current Members: {member.guild.member_count}"]
        
        if e:
            embed = discord.Embed(title=f"User Joined!",
                                description='\n'.join(value),
                                color=self.bot.color
                                )
            embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
            embed.set_footer(text=self.bot.footer)
            c = self.bot.get_channel(e)
            await c.send(embed=embed)

    # Reaction Role
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = payload.guild_id

        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", guild)
        role, vchannel = s['role'], s['vchannel']

        g = self.bot.get_guild(guild)
        r = g.get_role(role)
        m = g.get_member(payload.user_id)

        try:
            if m.bot:
                pass
            else:
                if int(payload.channel_id) == int(vchannel) and str(payload.emoji) == '\U00002705':
                    try:
                        await m.add_roles(r, reason="Verification")
                    except:
                        await g.owner.send(f'I could not verify {m.mention} due to an error. You might want to add the `{r.name}` ({r.id}) role to them to manually verify them.')
        except:
            pass
        
    # Commands    
    @commands.command(aliases=['set'])
    @commands.has_permissions(manage_guild=True)
    async def settings(self, ctx):
        '''See the toggleable guild settings.'''
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", ctx.guild.id)
        error = discord.Embed(title="⚠️ Error", description="There was a problem with getting your guilds data.\nThis means that your guild is not in my database.\nPlease [re-invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot) and run this command again.", color=self.bot.color)
        if not s: return await ctx.send(embed=error)
                 
        prefix, channel, role, vchannel = s['prefix'], s['channel'], s['role'], s['vchannel']
                 
        channel = ctx.guild.get_channel(channel)
        role = ctx.guild.get_role(role)
        vchannel = ctx.guild.get_channel(vchannel)

        embed = discord.Embed(title=f"{ctx.guild} Settings", description=f"**Prefix:** `{prefix}`", color=self.bot.color)
        embed.add_field(name=f"**Logging:** {on if channel else off}", value=f"> {channel.mention if channel is not None else 'No Channel Set'}", inline=False)
        embed.add_field(name=f"**Verify:** {on if role and vchannel is not None else off}", value=f"> {role.mention} {vchannel.mention}" if role and vchannel is not None else '> No Channel or Role Set', inline=False)
        embed.set_footer(text=self.bot.footer)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix:str):
        '''Change the command Prefix'''
        try:
            await self.bot.db.execute("UPDATE guilds SET prefix = $1 WHERE guildid = $2", str(prefix), ctx.guild.id)
            await ctx.send(f'Set the prefix to **`{prefix}`**')
            try:
                await ctx.guild.me.edit(nick=f'[{prefix}] Sirk')
            except:
                pass
        except Exception as e:
            await ctx.send(f'Error in setting prefix.\n```py\nError:\n{e}```')

    @commands.group(aliases=['log'])
    @commands.has_permissions(manage_guild=True)
    async def logging(self, ctx):
        """Logging commands."""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
            
    @logging.command()
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx, *, channel: discord.TextChannel):
        '''
        Set the logging channel\n*Note: You need to toggle logging before it starts logging.*
        '''
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", ctx.guild.id)
        error = discord.Embed(title="⚠️ Error", description="There was a problem with getting your guilds data.\nThis means that your guild is not in my database.\nPlease [re-invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot) and run this command again.", color=self.bot.color)
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

    @logging.command()
    @commands.has_permissions(manage_guild=True)
    async def stop(self, ctx):
        '''
        Remove the logging channel\n*Note: If this is removed, and logging is toggled on, it still will not log.*
        '''
        s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", ctx.guild.id)
        error = discord.Embed(title="⚠️ Error", description="There was a problem with getting your guilds data.\nThis means that your guild is not in my database.\nPlease [re-invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot) and run this command again.", color=self.bot.color)
        if not s: return await ctx.send(embed=error)
        try:
            await self.bot.db.execute("UPDATE guilds SET channel = $1 WHERE guildId = $2 ", None, ctx.guild.id)
            await ctx.send(f'Removed your logging channel.')
        except Exception as e:
            return await ctx.send(f"Something went wrong, please try again.\n\nError:```py\n{e}```")

    @commands.group()
    @commands.has_permissions(manage_guild=True)
    async def verify(self, ctx):
        """Verification commands."""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @verify.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def create(self, ctx, channel : discord.TextChannel, role : discord.Role):
        '''
        Setup React-to-Verify\n#channel @role
        '''
        c = ctx.guild.get_channel(channel.id)
        r = ctx.guild.get_role(role.id)
        await self.bot.db.execute("UPDATE guilds SET vchannel = $1, role = $2 WHERE guildid = $3", c.id, r.id, ctx.guild.id)
        await ctx.send(f"Set your verification channel to {c.mention} and your verification role to {r.mention}")
        if r > ctx.me.top_role:
            await ctx.send(f"In order for me to add roles to people, please put my role **HIGHER** than the {r.mention} role.")

        c = await config.Verify_Check(self, ctx.guild.id)

        if c:
            c = ctx.guild.get_channel(c)
            embed = discord.Embed(title="Verify", description="React to this message to gain access to the rest of the server.", color=self.bot.color)
            m = await c.send(embed=embed)
            await m.add_reaction('\U00002705')


    @verify.command()
    @commands.has_permissions(manage_guild=True)
    async def reset(self, ctx):
        '''
        Reset role and channel for verification.
        '''
        await self.bot.db.execute("UPDATE guilds SET role = $1, vchannel = $2 WHERE guildid = $3", None, None, ctx.guild.id)
        await ctx.send(f"Reset your verification settings.")

def setup(bot):
    bot.add_cog(config(bot))
