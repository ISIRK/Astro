import discord
from discord.ext import commands
from asyncio import sleep

class Mod(commands.Cog):
    """Commands for managing Discord servers."""
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member=None):
        """Kicks a user from the server."""
        if user == None:
            await ctx.send("User is a required argument that is missing.")
        elif ctx.author == user:
            await ctx.send("You cannot kick yourself.")
        else:
            await user.kick()
            embed = discord.Embed(title=f'User {user.name} has been kicked.', color=0x2F3136)
            embed.add_field(name="Bai!", value=":wave:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.Member=None):
        """Bans a user from the server."""
        if user == None:
            await ctx.send("User is a required argument that is missing.")
        if ctx.author == user:
            await ctx.send("You cannot ban yourself.")
        else:
            await user.ban()
            embed = discord.Embed(title=f'User {user.name} has been banned.', color=0x2F3136)
            embed.add_field(name="Bai!", value=":hammer:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user : discord.Member, time: int):
        """Prevents a user from speaking for a specified amount of time."""
        if ctx.author == user:
            await ctx.send("You cannot mute yourself.")
        else:
            rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
            if rolem is None:
                embed=discord.Embed(title="Muted role", url="http://echo-bot.wikia.com/wiki/Setting_up_the_muted_role", description="The mute command requires a role named 'Muted'.", color=0x2F3136)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                embed.set_footer(text="Without this role, the command will not work.")
                await ctx.send(embed=embed)
            elif rolem not in user.roles:
                embed = discord.Embed(title=f'User {user.name} has been successfully muted for {time}s.', color=0x2F3136)
                embed.add_field(name="Shhh!", value=":zipper_mouth:")
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)
                await user.add_roles(rolem)
                await sleep(time)
                if rolem in user.roles:
                    try:
                        await user.remove_roles(rolem)
                        embed = discord.Embed(title=f'User {user.name} has been automatically unmuted.', color=0x2F3136)
                        embed.add_field(name="Welcome back!", value=":open_mouth:")
                        embed.set_thumbnail(url=user.avatar_url)
                        await ctx.send(embed=embed)
                    except Exception:
                        print(f'User {user.name} could not be unmuted!')
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
    async def clear(self, ctx, count: int=None):
        """Deletes a specified amount of messages. (Max 100)"""
        if count == None:
            await ctx.send("Number is a required argument that is missing.")
        else:
            if count>100:
                count = 100
            await ctx.message.channel.purge(limit=count+1, bulk=True)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int=None):
        '''Change the slowmode in the current channel.'''
        if seconds == None:
            await ctx.send("Seconds is a required argument that is missing.")
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(f"Slowmode is now {seconds} seconds.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self , ctx, user : discord.Member=None, *, reason=None):
        '''Warn a Member'''
        if user == None:
            await ctx.send("User is a required argument that is missing.")
        elif reason == None:
            await ctx.send("Reason is a required argument that is missing.")
        else:
            guild = ctx.guild
            embed = discord.Embed(color=0x2F3136)
            embed.set_author(name=f"Warned By {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"You Have Been Warned in {guild}\n\nReason:", value=f'{reason}')
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758453150897799172.png?v=1")
            await user.send(embed=embed)
            await ctx.send(f"<:help:758453150897799172> Warned {user}")

def setup(bot):
    bot.add_cog(Mod(bot))
