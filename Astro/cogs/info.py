from multiprocessing.connection import Client
import discord
from discord import Embed
from discord.ext import commands
from discord.shard import ShardInfo
from discord.user import User
from discord.utils import get
from datetime import datetime
import os
import collections
import time, datetime
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        '''Get information about the bot.'''
        infoembed = discord.Embed(title="Info", description="A Utilities Discord Bot with reliability and simplicity", color=0x2F3136)
        infoembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        infoembed.add_field(name= "<:news:758781954073821194> News", value="**<:dev:759427919302492160> <@751447995270168586> Is Now PUBLIC! <:dev:759427919302492160>**\nTo invite Astro either click [here](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&redirect_uri=https%3A%2F%2Fastrobot.carrd.co%2F&response_type=code&scope=bot%20identify), [here](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&redirect_uri=https%3A%2F%2Fastrobot.carrd.co%2F&response_type=code&scope=bot%20identify), or [here](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&redirect_uri=https%3A%2F%2Fastrobot.carrd.co%2F&response_type=code&scope=bot%20identify).\nOr you can type `[prefix]invite` to get invite info!", inline=True)
        infoembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758451109919981580.png?v=1")
        infoembed.add_field(name= ":link: Links", value="[Invite](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&redirect_uri=https%3A%2F%2Fastrobot.carrd.co%2F&response_type=code&scope=bot%20identify)\n[Bot Site](https://asksirk.com/Astro) \n[Github Repository](https://github.com/ISIRK/Astro) \n[Patreon](https://www.patreon.com/Astro_Bot)", inline=False)
        infoembed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=infoembed)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        supportembed = discord.Embed(title="Support", color=0x2F3136)
        supportembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        supportembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758453150897799172.png?v=1")
        supportembed.add_field(name="Support Server", value="<:discord:765251798629220382> Support Server: https://discord.gg/7yZqHfG", inline=False)
        supportembed.add_field(name="Contact", value="To contact dm isirk#0001 or email me @ isirk@asksirk.com", inline=False)
        #supportembed.add_field(name=":link: Links", value="Bot Site: https://asksirk.com/Astro\nGithub Repository: https://github.com/ISIRK/Astro\nPatreon: https://www.patreon.com/Astro_Bot", inline=False)
        supportembed.set_footer(text="Use [prefix] help or info.")
        await ctx.send(embed=supportembed)
    
    @commands.command()
    async def invite(self , ctx):
        '''Get the invite for the bot.'''
        embed = discord.Embed(title="Invite", color=0x2F3136)
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://asksirk.com/Astro/astronaut.jpg")
        embed.add_field(name="Invite Link:", value="🌐 [Invite Link](https://discord.com/oauth2/authorize?client_id=751447995270168586&permissions=268823638&redirect_uri=https%3A%2F%2Fastrobot.carrd.co%2F&response_type=code&scope=bot%20identify)", inline=False)
        embed.add_field(name="Support Server:", value="<:discord:765251798629220382> [Support Server](https://discord.gg/7yZqHfG)", inline=False)
        embed.add_field(name="Contact:", value="To contact dm isirk#0001 or email me @ isirk@asksirk.com", inline=False)
        embed.set_footer(text="Use [prefix] help or info.")
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *, page=None):
        
        helpembed1 = discord.Embed(title="Help", description="A Utilities Discord Bot with reliability and simplicity\n Made By isirk#0001", color=0x2F3136)
        helpembed1.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        helpembed1.add_field(name="Prefix", value="`@Astro ,Astro ,astro ,^`", inline=False)
        helpembed1.add_field(name= "Help", value="React below to change the pages.\n**Note:**\n**You can type `help <page name>` to get a specific help page.**", inline=False)
        helpembed1.add_field(name="Pages", value="```yaml\n1) Info\n2) Utility\n3) Mod\n4) Other\n```", inline=False)
        helpembed1.add_field(name="About", value="Version 1.0 **Public Beta**\nMade with :heart: in <:python:758139554670313493>\nOwned, Developed, and Run by isirk#0001", inline=False)
        helpembed1.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        
        info = discord.Embed(title="Info", description="Information Commands", color=0x2F3136)
        info.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        info.add_field(name="Syntax:", value="```yaml\n<input> - Input for the Command\n[o] - Optional\n```", inline=False)
        info.add_field(name="Commands:", value="`info` - Get Info About the Bot.\n`invite` - Get the invite for Astro.\n`support` Get Support Information.\n`privacy` - Privacy Policy for Astro.\n`help <[o]page name>` - This Message *or* a specific Help Page", inline=False)
        info.set_footer(text="Astro Bot | discord.gg/7yZqHfG")

        utility = discord.Embed(title="Utility", description="Utiity Commands", color=0x2F3136)
        utility.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        utility.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        utility.add_field(name="Syntax:", value="```yaml\n<input> - Input for the Command\n[o] - Optional\n```", inline=False)
        utility.add_field(name="Commands:", value="`avatar|av <[o]mention>` - Get the avatar of the mentioned user.\n`ping` - Get the Bot Ping.\n`server` - Get Info About The Server.\n`stats` - Get the Bot Stats.\n`user <[o]mention>` - Get the Stats of the Mentioned User.", inline=False)
        
        mod = discord.Embed(title="Mod", description="Moderation Commands\***Note you need specific permissions for each command.***", color=0x2F3136)
        mod.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        mod.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        mod.add_field(name="Syntax:", value="```yaml\n<input> - Input for the Command\n(permission) - Required Permissions```", inline=False)
        mod.add_field(name="Commands:", value="`kick <user>` - Kick the mentioned user from the server. (`kick_members`)\n`ban <user>` - Ban the mentioned user from the server. (`ban_members`)\n`warn <user> <reason>` - Warn A User for a Specified Reason.(`kick_members`)\n`clear <#>` - Delete a number of messages. **Max 100** (`manage_messages`)\n`slowmode <seconds>` - Change the Channel Slowmode to a specified number of seconds. (`manage_channels`)\n~~~`mute <user>` - Mute a User.~~~ (Re-Working)\n~~~`unmute <user>` - Un-mutes a User.~~~ (Re-Working)", inline=False)
        
        other = discord.Embed(title="Other", description="Other Commands", color=0x2F3136)
        other.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        other.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        other.add_field(name="Commands:", value="`dice` - Roll A Dice (*There is a possibility you'll get a mystery.*)", inline=False)
        
        if page == "info":
            await ctx.send(embed=info)
        elif page == "utility":
            await ctx.send(embed=utility)
        elif page == "mod":
            await ctx.send(embed=mod)
        elif page == "other":
            await ctx.send(embed=other)
        else:
            embeds = [
            helpembed1,
            info,
            utility,
            mod,
            other,
            Embed(title="End!", description="More to come...", color=discord.Colour.blurple())
        ]

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()
        
    @commands.command()
    async def privacy(self, ctx):
        embed = discord.Embed(title="Privacy Policy for Astro", description="Astro strives to store no data to make astro as simple to use as possible.\nNothing is stored, recorded or anything of that sort.\n\n<:tab:758139554842148934> [Privacy Policy](https://asksirk.com/Astro/privacy/)", color=0x2F3136)
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=embed)
     
def setup(bot):
    bot.add_cog(info(bot))
