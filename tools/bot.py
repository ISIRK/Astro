import discord
from discord.ext import commands, tasks
from datetime import datetime
import aiohttp
import os
import asyncio
import asyncpg
import json
import tools.utils as utils

tokenFile = "tools/config.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data['TOKEN']
user = data['DB-USER']
password = data['DB-PWD']
name = data['DB-NAME']

intents = discord.Intents.default()
intents.members = True

async def get_prefix(bot, message : discord.Message):
    '''
    Get Prefix
    '''
    try:
        s = await bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", message.guild.id)
        p = str(s['prefix'])

        if message.author.id == bot.owner_id:
            return commands.when_mentioned_or(p, "")(bot, message)
        else:
            return commands.when_mentioned_or(p)(bot, message)
    except:
        await bot.db.execute("INSERT INTO guilds (guildId) VALUES($1)", message.guild.id)
        pass

class Sirk(commands.Bot):
    """
    Subclassed bot.
    """
    def __init__(self):
        super().__init__(        
            command_prefix=get_prefix,
            intents=intents, case_insensitive=True, 
            allowed_mentions=discord.AllowedMentions(users=True, roles=True, everyone=False, replied_user=False),
            owner_id=542405601255489537,
            description="A minimalistic bot for discord Developed by isirk#0001"
        )       
        self.uptime = datetime.utcnow()
        self.session = aiohttp.ClientSession()
        self.db = asyncio.get_event_loop().run_until_complete(asyncpg.create_pool(user=user, password=password, database=name, host='127.0.0.1'))
        self.footer = "Sirk Bot v2.0.1"
        self.color = 0x7289DA
        self.utils = utils

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return
        elif after.author.id == self.owner_id:
            await self.process_commands(after)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        elif not message.guild:
            pass
        elif (
            message.content == f"<@!{self.user.id}>"
            or message.content == f"<@{self.user.id}>"
        ):
            s = await self.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", message.guild.id)
            p = str(s['prefix'])
            await message.channel.send(embed=discord.Embed(title="Prefix", description=f"My prefix for {message.guild.name} are {self.user.mention} and `{p}`", color=self.color))
        await self.process_commands(message)

    async def mystbin(self, data):
        async with self.session.post('https://mystb.in/documents', data=data) as r:
            return f"https://mystb.in/{(await r.json())['key']}"
    
    async def say(self, ctx, *, text):
        return await ctx.send(f'{str(text)}')
