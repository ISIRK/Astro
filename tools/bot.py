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
    Custom Prefix
    '''
    try:
        s = await bot.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", message.guild.id)
        p = str(s['prefix'])
        
        return commands.when_mentioned_or(p)(bot, message)
    except:
        await bot.db.execute("INSERT INTO guilds (guildId) VALUES($1)", message.guild.id)
        pass

class Sirk(commands.Bot):
    '''
    Custom Bot
    '''
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
        self.footer = "Sirk Bot v1"
        self.color = 0x7289DA
        self.utils = utils

        @self.check
        async def global_check(ctx):
            bl = await self.db.fetchrow("SELECT * FROM blacklist WHERE id = $1", ctx.author.id)
            if bl:
                await ctx.send(embed=discord.Embed(description=f"You have been blacklisted for `{bl['reason']}`",color=discord.Color.red()))
                return False

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
            return
        elif (
            message.content == f"<@!{self.user.id}>"
            or message.content == f"<@{self.user.id}>"
        ):
            s = await self.db.fetchrow("SELECT prefix FROM guilds WHERE guildid = $1", message.guild.id)
            p = str(s['prefix'])
            await message.channel.send(embed=discord.Embed(title="Prefix", description=f"My prefixes for {message.guild.name} are {self.user.mention} and `{p}`", color=self.color))
        await self.process_commands(message)

    async def get_context(self, message: discord.Message, *, cls=None):
        return await super().get_context(message, cls=cls or Context)

class Context(commands.Context):
    '''
    Custom Context
    '''
    async def remove(self, *args, **kwargs):
        m = await self.send(*args, **kwargs)
        await m.add_reaction('🇽')
        try:
            await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == self.author.id and r.message.id == m.id and str(r.emoji) == '🇽', timeout=60.0)
            await m.delete()
        except asyncio.TimeoutError:
            pass
