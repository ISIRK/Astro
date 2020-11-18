import discord
from discord.ext import commands
import json
import asyncio
from asyncio import sleep
import typing

colorfile = "/home/pi/Discord/Sirk/utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data['COLORS'], 16)

class mod(commands.Cog):
    '''Moderation Commands\n*Note: These commands required specific permissions.*'''
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member):
        """Kicks a user from the server."""
        if ctx.author == user:
            await ctx.send("You cannot kick yourself.")
        if user.top_role >= ctx.author.top_role and ctx.author.id != 542405601255489537:
            await ctx.send("You can only kick people below you in role hierarchy.")
            return
        else:
            await user.kick()
            embed = discord.Embed(title=f'User {user.name} has been kicked.', color=color)
            embed.add_field(name="Bai!", value=":wave:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: typing.Union[discord.Member, discord.User]):
        """Bans a user from the server."""
        if ctx.author == user:
            await ctx.send("You cannot ban yourself.")
        if user.top_role >= ctx.author.top_role and ctx.author.id != 542405601255489537:            
            await ctx.send("You can only ban people below you in role hierarchy.")
            return
        else:
            # If user is not in the guild ban the user's object
            if isinstance(user, discord.User):
                user = discord.Object(user.id)

            await ctx.guild.ban(user)
            
            embed = discord.Embed(title=f'User {user.name} has been banned.', color=color)
            embed.add_field(name="Bai!", value=":hammer:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member, reason: str = None):
        """Prevents a user from speaking"""
        permissions = discord.Permissions(1049600)
        if ctx.author == user:
            await ctx.send("You cannot mute yourself.")
        else:
            rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
            if rolem is None:
                rolem = await ctx.guild.create_role(name="Muted", permissions=permissions, hoist=False, color=discord.Color.light_gray())
            elif rolem not in user.roles:
                await ctx.author.add_roles(rolem, reason=reason)
                embed = discord.Embed(title=f'User {user.name} has been successfully muted.', color=0x2F3136)
                embed.add_field(name="Shhh!", value=":zipper_mouth:")
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'User {user.mention} is already muted.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, user: discord.Member):
        """Unmutes a user."""
        rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
        if rolem in user.roles:
            embed = discord.Embed(title=f'User {user.name} has been manually unmuted.', color=0x2F3136)
            embed.add_field(name="Welcome back!", value=":open_mouth:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
            await user.remove_roles(rolem)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        """Deletes a specified amount of messages. (Max 100)"""
        if count>100:
            count = 100
        await ctx.message.channel.purge(limit=count+1, bulk=True)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
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
            embed = discord.Embed(color=color)
            embed.set_author(name=f"Warned By {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"You Have Been Warned in {guild}\n\nReason:", value=f'{reason}')
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758453150897799172.png?v=1")
            await user.send(embed=embed)
            await ctx.send(f"<:help:758453150897799172> Warned {user}")

    @commands.command(aliases=['em'])
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, channel: discord.TextChannel):
        '''Make a custom embed and send it in any channel'''
        await ctx.send("Embed Maker Started\nWhat would you like the title to be?")
        try:
            title = await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await ctx.send('Timeout Error')
        else: 
            await ctx.send("What would you like the description to be?")
            try:
                description = await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
            except asyncio.TimeoutError:
                await ctx.send('Timeout Error')
            else:
                embed = discord.Embed(title=title.content, description=description.content, color=color)
                await channel.send(embed=embed)
                await ctx.send(f'`{title.content}` Embed sent in #{channel}')

def setup(bot):
    bot.add_cog(mod(bot))
