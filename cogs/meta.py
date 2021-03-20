import discord, os, collections, time, datetime, random, psutil, json, platform, inspect, sys, multiprocessing, asyncio, humanize, typing
from collections import Counter
from discord.ext import commands
from discord.ext.commands import BucketType

class meta(commands.Cog):
    '''Meta commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['info'])
    async def about(self, ctx):
        """Displays bot info"""
        mem = psutil.virtual_memory()
        embed = discord.Embed(title="Bot Info", color=self.bot.color)
        owner = self.bot.get_user(self.bot.owner_id)
        embed.set_author(name=str(owner), icon_url=owner.avatar_url)
        embed.set_footer(text=self.bot.footer)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="About",
                        value=f"{self.bot.description}"
                       )
        embed.add_field(name=f"Stats",
                        value=f"Servers: {len(self.bot.guilds)}\nUsers: {len(self.bot.users):,}\nCommands: {len(self.bot.commands)}"
                       )
        embed.add_field(name="Usage:",
                        value=f"```CPU Usage: {psutil.cpu_percent()}%\n{mem[1] / 1000000:.3f} MB available ({100 - mem[2]:.2f}%)```",
                        inline=False)
        embed.add_field(name="Version Info",
                        value=f"```Python: {platform.python_version()}\nDiscord.py: {discord.__version__}```")
        embed.add_field(name="Links",
                        value="[Support Server](https://discord.gg/7yZqHfG)\n[Website](https://asksirk.com/bot/)\n[TOP.GG](https://top.gg/bot/751447995270168586/) [BotList.Space](https://botlist.space/bot/751447995270168586)")
        await ctx.send(embed=embed)
        
    @commands.command()
    async def credits(self, ctx):
        '''See the credits for Sirk'''
        embed = discord.Embed(title="Credits", description="Many thanks to these people who helped:\nCraziiAce#0001, Cyrus#8315, Moksej#3335, Preselany#6969, Vaskel#6969, PB#4162", color=self.bot.color)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=self.bot.footer)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def vote(self, ctx):
        embed = discord.Embed(title="Vote", description="[Top.GG](https://top.gg/bot/751447995270168586/)\n[BotList.Space](https://botlist.space/bot/751447995270168586)\n[Discord Extreme List](https://discordextremelist.xyz/en-US/bots/sirk)", color=self.bot.color)
        embed.set_footer(text=self.bot.footer)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        await ctx.send('https://discord.gg/7yZqHfG')
    
    @commands.command()
    async def invite(self , ctx):
        '''Get the invite for the bot.'''
        await ctx.send('<https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&scope=bot>')
        
    @commands.command()
    async def privacy(self, ctx):
        '''See the bots privacy policy'''
        embed = discord.Embed(title="Privacy Policy for Sirk Bot", url="https://asksirk.com/bot/privacy/", color=self.bot.color)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        '''Get the bot ping'''
        try:
            await ctx.message.add_reaction('🏓')
        except:
            pass
        await ctx.send(f"Pong! Average Latency is {round(self.bot.latency * 1000)} ms")
        
    @commands.command()
    async def uptime(self, ctx):
        """Displays the uptime"""
        await ctx.send(f"{humanize.precisedelta(self.bot.uptime, format='%0.0f')}")

    @commands.command()
    async def server(self, ctx):
        '''Get information about the server.'''
        guild = ctx.guild
        
        embed = discord.Embed(title=f"{guild.name}", color=self.bot.color)
        embed.description = guild.description if guild.description else None
        embed.add_field(name='**General:**',
                        value=f'Owner: **{guild.owner}**\n'
                              f'Created on: **{datetime.datetime.strftime(guild.created_at, "%A %d %B %Y at %H:%M")}**\n'
                              f'Members: **{guild.member_count}**\n'
                              f'Bots: **{len([x for x in guild.members if x.bot])}**\n'
                              f'Boost: **Tier {guild.premium_tier}**\n'
                              f'Region: **{guild.region}**\n'
                              f'Boosters: **{guild.premium_subscription_count}**\n'
                              f'Max File Size: **{round(guild.filesize_limit / 1048576)} MB**\n'
                              f'Bitrate: **{round(guild.bitrate_limit / 1000)} kbps**\n'
                              f'Max Emojis: **{guild.emoji_limit}**\n'
                              f'Emojis: **{" ".join(str(e) for e in guild.emojis[:5])} + {len(guild.emojis) - 5} more**', inline=False)

        embed.add_field(name='**Channel Information:**',
                        value=f'AFK timeout: **{int(guild.afk_timeout / 60)}m**\n'
                              f'AFK channel: **{guild.afk_channel}**\n'
                              f'<:textchannel:724637677395116072> **{len(guild.text_channels)}**\n'
                              f'<:voicechannel:724637677130875001> **{len(guild.voice_channels)}**\n', inline = False)

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_image(url=guild.banner_url)
        embed.set_footer(text=f'Guild ID: {guild.id} | {self.bot.footer}')

        return await ctx.send(embed=embed)

    @commands.command(aliases=['whois', 'ui'])
    async def user(self, ctx, *, member: discord.Member = None):
        '''Get information about the mentioned user.'''
        if member is None:
            member = ctx.author
            
        roles = ' '.join([r.mention for r in member.roles[:10] if r != ctx.guild.default_role] or ['None'])
        shared = sum(g.get_member(member.id) is not None for g in self.bot.guilds)
        
        embed = discord.Embed(title=f"{member}", color=member.color)
        embed.add_field(name='**General:**',
                        value=f'Name: **{member}**\n' 
                              f'Bot: **{"Yes" if member.bot else "No"}**\n'
                              f'Shared Guilds: **{shared}**\n'
                              f'Account Created on: **{datetime.datetime.strftime(member.created_at, "%A %d %B %Y at %H:%M")}**', inline=False)

        embed.add_field(name='**Guild related information:**',
                        value=f'Joined guild: **{datetime.datetime.strftime(member.joined_at, "%A %d %B %Y at %H:%M")}**\n'
                              f'Nickname: **{member.nick}**\n'
                              f'Roles: {roles}', inline=False)

        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'Member ID: {member.id} | {self.bot.footer}')

        return await ctx.send(embed=embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, member: discord.Member = None):
        '''Display a member's avatar'''
        av = member or ctx.author
        await ctx.send(embed=discord.Embed(color=0x2F3136).set_author(name=av).set_image(url=av.avatar_url))
                        
    @commands.command(name="perms")
    async def permissions(self, ctx, *, member: discord.Member=None):
        '''A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked.'''
        if not member:
            member = ctx.author

        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions', description=f"```md\n{perms}```", colour=self.bot.color)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.set_footer(text=self.bot.footer)
        await ctx.send(content=None, embed=embed)

    @commands.command()
    async def raw(self, ctx, id: discord.Message = None):
        '''Get the raw contents of a message.'''
        msg = id or ctx.message
        raw = json.dumps(await self.bot.http.get_message(ctx.channel.id, msg.id), indent=4)
        await ctx.send(embed = discord.Embed(description=f'```json\n{raw}```', color=self.bot.color))

    @commands.command()
    async def id(self, ctx, *, thing: typing.Union[discord.PartialEmoji, discord.Role, discord.Member, discord.TextChannel, discord.VoiceChannel, discord.Emoji]):
        '''Get the id for something'''
        await ctx.send(f"{thing.id}")
                        
def setup(bot):
    bot.add_cog(meta(bot))
