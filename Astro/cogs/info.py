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

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        '''Get information about the bot.'''
        infoembed = discord.Embed(title="Info", description="A Utilities Discord Bot with reliability and simplicity", color=0x7289DA)
        infoembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        infoembed.add_field(name= "<:news:758781954073821194> News", value="<:translate:758449663517917195> Translators Needed. <:translate:758449663517917195>\nIf you can speak another language fluently or know someone who can DM isirk#0001.", inline=True)
        infoembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758451109919981580.png?v=1")
        infoembed.add_field(name= ":link: Links", value="[Bot Site](https://asksirk.com/Astro) \n[Github Repository](https://github.com/ISIRK/Astro) \n[Patreon](https://www.patreon.com/Astro_Bot)", inline=False)
        infoembed.add_field(name="About", value="Version 1.0 **Public Beta**\nMade with :heart: in <:python:758139554670313493>\nOwned, Developed, and Run by isirk#0001", inline=False)
        infoembed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")
        await ctx.send(embed=infoembed)

    @commands.command()
    async def help1(self, ctx):
        '''Old/New help command that is being worked on right now.'''
        helpembed = discord.Embed(title="Help", description="A Utilities Discord Bot with reliability and simplicity\n Made By isirk#0001", color=0x7289DA)
        helpembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        helpembed.add_field(name="Prefix", value="`^` (Not Customizeable)", inline=False)
        helpembed.add_field(name="Bot", value="`help`\n`info`\n`ping`\n`support`")
        helpembed.add_field(name="Mod", value="`kick`\n`ban`\n`mute`\n`unmute`")
        helpembed.add_field(name="Utility", value="`avatar`\n`slowmode`\n`clear`\n`server`\n`user`")
        helpembed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")

        await ctx.send(embed=helpembed)

    @commands.command()
    async def support(self, ctx):
        '''Get support information.'''
        supportembed = discord.Embed(title="Support", color=0x7289DA)
        supportembed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        supportembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/758453150897799172.png?v=1")
        supportembed.add_field(name="Support Server", value="Support Server: https://discord.gg/7yZqHfG", inline=False)
        supportembed.add_field(name="Contact", value="To contact dm isirk#0001 or email me @ isirk@asksirk.com", inline=False)
        supportembed.add_field(name=":link: Links", value="Bot Site: https://asksirk.com/Astro\nGithub Repository: https://github.com/ISIRK/Astro\nPatreon: https://www.patreon.com/Astro_Bot", inline=False)
        supportembed.set_footer(text="Use [prefix] help or info.")
        await ctx.send(embed=supportembed)
    
    @commands.command()
    async def invite(self , ctx):
        '''Get the invite for the bot.'''
        embed = discord.Embed(title="Invite", color=0x7289DA)
        embed.add_field(name="Contact", value="Unfortunately Astro Bot is a Private Bot.\nIf You want to invite Astro into your server\n**DM isirk#0001 on discord with the format below:**\n```\nName:(Discord Tag)\nServer Name:\nServer Invite:\nAmmount of Members:\nWhy you want Astro in your server:\n(Optional)Any other thing you want me to know?\n```", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758138226874908705/758729610237837372/astro.png")
        await ctx.send(embed=embed)
    
    
	@commands.command(pass_context=True)
	async def about(self, ctx):
		"""Lists some general stats about the bot."""
		bot_member = self.bot.user if not ctx.guild else ctx.guild.get_member(self.bot.user.id)
		color = bot_member if isinstance(bot_member,discord.Member) else None
		message = await Message.EmbedText(title="Gathering info...", color=color).send(ctx)
		
		# Get guild count
		guild_count = "{:,}".format(len(self.bot.guilds))
		
		# Try to do this more efficiently, and faster
		total_members = [x.id for x in self.bot.get_all_members()]
		unique_members = set(total_members)
		if len(total_members) == len(unique_members):
			member_count = "{:,}".format(len(total_members))
		else:
			member_count = "{:,} ({:,} unique)".format(len(total_members), len(unique_members))
			
		# Get commands/cogs count
		cog_amnt  = 0
		empty_cog = 0
		for cog in self.bot.cogs:
			visible = []
			for c in self.bot.get_cog(cog).get_commands():
				if c.hidden:
					continue
				visible.append(c)
			if not len(visible):
				empty_cog +=1
				# Skip empty cogs
				continue
			cog_amnt += 1
		
		cog_count = "{:,} cog".format(cog_amnt)
		# Easy way to append "s" if needed:
		if not len(self.bot.cogs) == 1:
			cog_count += "s"
		if empty_cog:
			cog_count += " [{:,} without commands]".format(empty_cog)

		visible = []
		for command in self.bot.commands:
			if command.hidden:
				continue
			visible.append(command)
			
		command_count = "{:,}".format(len(visible))
		
		# Get localized created time
		local_time = UserTime.getUserTime(ctx.author, self.settings, bot_member.created_at)
		created_at = "{} {}".format(local_time['time'], local_time['zone'])
		
		# Get localized joined time if in a server
		if isinstance(bot_member,discord.Member):
			local_time = UserTime.getUserTime(ctx.author, self.settings, bot_member.joined_at)
			joined_at = "{} {}".format(local_time['time'], local_time['zone'])
		
		# Get the current prefix
		prefix = await self.bot.command_prefix(self.bot, ctx.message)
		prefix = ", ".join([x for x in prefix if not x == "<@!{}> ".format(self.bot.user.id)])

		# Get the owners
		ownerList = self.settings.getGlobalStat('Owner',[])
		owners = "Unclaimed..."
		if len(ownerList):
			userList = []
			for owner in ownerList:
				# Get the owner's name
				user = self.bot.get_user(int(owner))
				if not user:
					userString = "Unknown User ({})".format(owner)
				else:
					userString = "{}#{}".format(user.name, user.discriminator)
				userList.append(userString)
			owners = ', '.join(userList)
			
		# Get bot's avatar url
		avatar = bot_member.avatar_url
		if not len(avatar):
			avatar = bot_member.default_avatar_url
		
		# Build the embed
		fields = [
			{"name":"Members","value":member_count,"inline":True},
			{"name":"Servers","value":guild_count,"inline":True},
			{"name":"Commands","value":command_count + " (in {})".format(cog_count),"inline":True},
			{"name":"Created","value":created_at,"inline":True},
			{"name":"Owners","value":owners,"inline":True},
			{"name":"Prefixes","value":prefix,"inline":True},
			{"name":"Shard Count","value":self.bot.shard_count,"inline":True}
		]
		if isinstance(bot_member,discord.Member):
			fields.append({"name":"Joined","value":joined_at,"inline":True})
			# Get status
			status_text = ":green_heart:"
			if bot_member.status == discord.Status.offline:
				status_text = ":black_heart:"
			elif bot_member.status == discord.Status.dnd:
				status_text = ":heart:"
			elif bot_member.status == discord.Status.idle:
				status_text = ":yellow_heart:"
			fields.append({"name":"Status","value":status_text,"inline":True})

			if bot_member.activity and bot_member.activity.name:
				play_list = [ "Playing", "Streaming", "Listening to", "Watching" ]
				try:
					play_string = play_list[bot_member.activity.type]
				except:
					play_string = "Playing"
				fields.append({"name":play_string,"value":str(bot_member.activity.name),"inline":True})
				if bot_member.activity.type == 1:
					# Add the URL too
					fields.append({"name":"Stream URL","value":"[Watch Now]({})".format(bot_member.activity.url),"inline":True})
		# Update the embed
		await Message.Embed(
			title=DisplayName.name(bot_member) + " Info",
			color=color,
			description="Current Bot Information",
			fields=fields,
			thumbnail=avatar
		).edit(ctx, message)

def setup(bot):
    bot.add_cog(info(bot))
