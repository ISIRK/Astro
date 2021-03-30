import discord
from discord.ext import commands
import json
import asyncio
from asyncio import sleep
import typing

class mod(commands.Cog):
    '''Moderation Commands\n*Note: These commands required specific permissions.*'''
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member):
        """Kicks a user from the server."""
        if ctx.author == user:
            await ctx.send("You cannot kick yourself.")
        if user.top_role >= ctx.author.top_role and ctx.author.id != 542405601255489537:
            await ctx.send("You can only kick people below you in role hierarchy.")
            return
        else:
            await user.kick()
            embed = discord.Embed(title=f'User {user.name} has been kicked.', color=self.bot.color)
            embed.add_field(name="Bai!", value=":wave:")
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=self.bot.footer)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a user"""
        if member.id == ctx.author.id:
            return await ctx.send("You can't do that to yourself!")
        if member.top_role >= ctx.me.top_role:
            return await ctx.send("That member's top role is higher or equal to mine!")

        guild = ctx.guild

        try:
            await member.send(f"You were banned from {guild.name} for {reason}")
        except:
            pass
        await guild.ban(member, reason=reason)
        await ctx.send(embed=discord.Embed(description=f"{member.name} was banned by {ctx.author.mention} for {reason}.", color=self.bot.color))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user: int, *, reason=None):
        """Unbans a user with a given ID"""
        if user == ctx.author.id:
            return await ctx.send("You can't do that to yourself!")
        member = discord.Object(id=user)
        try:
            await ctx.guild.unban(member, reason=reason)
            await ctx.send(embed=discord.Embed(description=f"Unbanned {member.id} for {reason}.", color=self.bot.color))
        except discord.NotFound:
            return await ctx.send(embed=discord.Embed(description="That user doesn't seem to be banned.", color=self.bot.color))

    '''@commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member, reason: str = None):
        """Prevents a user from speaking"""
        permissions = discord.Permissions(1049600)
        if ctx.author == user:
            await ctx.reply("You cannot mute yourself.")
        else:
            rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
            if rolem is None:
                rolem = await ctx.guild.create_role(name="Muted", permissions=permissions, hoist=False, color=discord.Color.light_gray())
            elif rolem not in user.roles:
                await user.add_roles(rolem, reason=reason)
                embed = discord.Embed(title=f'User {user.name} has been successfully muted.', color=0x2F3136)
                embed.add_field(name="Shhh!", value=":zipper_mouth:")
                embed.add_field(name="Note", value="If the Muted Role I created is lower than the members highest role they will not be muted.\nTo change this go into server settings and move the `Muted` role above their highest role.", inline=False)
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.reply(embed=embed)
            else:
                await ctx.reply(f'User {user.mention} is already muted.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, user: discord.Member):
        """Unmutes a user."""
        rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
        if rolem in user.roles:
            embed = discord.Embed(title=f'User {user.name} has been manually unmuted.', color=0x2F3136)
            embed.add_field(name="Welcome back!", value=":open_mouth:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.reply(embed=embed)
            await user.remove_roles(rolem)'''

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        """Deletes a specified amount of messages. (Max 100)"""
        await ctx.channel.purge(limit=count+1, bulk=True)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        '''Change the slowmode in the current channel.'''
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Slowmode is now {seconds} seconds.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self , ctx, user : discord.Member, *, reason):
        '''Warn a Member'''
        if user.top_role >= ctx.author.top_role and ctx.author.id != 542405601255489537:
            await ctx.send("You can only warn people below you in role hierarchy.")
            return
        else:
            guild = ctx.guild
            embed = discord.Embed(color=self.bot.color)
            embed.set_author(name=f"Warned By {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"You Have Been Warned in {guild}\n\nReason:", value=f'{reason}')
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758453150897799172.png?v=1")
            embed.set_footer(text=self.bot.footer)
            await user.send(embed=embed)
            await ctx.send(f"<:help:758453150897799172> Warned {user}")
            s = await self.bot.db.fetchrow("SELECT * FROM guilds WHERE guildid = $1", ctx.guild.id)
            logging = s['logging']
            channel = s['channel']
            c = self.bot.get_channel(channel)
            if logging:
                if channel:
                    await c.send('test')
                else:
                    pass
            else:
                pass


    @commands.command(aliases=['em'])
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, *, code: json.loads):
        '''
        Make a custom embed
        
        To make an embed use `{}` and insert your args.
        
        **args:** `title` `description` `author` `color` `footer` `fields`

        Example: ```{"title" : "This is the title","description" : "This is the description", "author" : {"name" : "The Author"}, "color" : 7506394, "footer" : {"text" : "This is the footer"}, "fields" : [{"name" : "Field Title", "value" : "Field Description", "inline" : false}]}```
        '''
        try:
         await ctx.send(embed=discord.Embed().from_dict(code))
        except Exception as e:
            await ctx.send(f'There was an error making the embed, use `{ctx.prefix}help {ctx.command}` for proper use.')

def setup(bot):
    bot.add_cog(mod(bot))
