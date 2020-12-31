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

import os

import asyncio

import discord

from discord.ext import commands, menus

from datetime import datetime

import json

import configparser, asyncpg, aiohttp

from typing import Tuple

##CONFIG
tokenFile = "tools/config.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data['TOKEN']
user = data['DB-USER']
password = data['DB-PWD']
name = data['DB-NAME']

prefixFile = "tools/tools.json"
with open(prefixFile) as f:
    data = json.load(f)
prefixes = data['PREFIXES']

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("^"), intents=intents, allowed_mentions=discord.AllowedMentions(users=True, roles=True, everyone=False, replied_user=False))
# Might Wanna look at this: command_prefix=commands.when_mentioned_or(prefixes)
bot.mentions: Tuple[str] = None

bot.start_time = datetime.utcnow()

bot.owner_ids = {542405601255489537}
#bot.remove_command('help')

#database
bot.loop = asyncio.get_event_loop()
bot.db = bot.loop.run_until_complete(asyncpg.connect(user=user, password=password, database=name, host='127.0.0.1'))

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

# also
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"


async def ainit():
    await bot.wait_until_ready()
    bot.mentions = (f"<@{bot.user.id}>", f"<@!{bot.user.id}>")


@bot.event
async def on_ready():
    print('{0.user} is up and running'.format(bot))
    # await bot.change_presence(status=discord.Status.idle)
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.mentions and message.content in bot.mentions:
        embed = discord.Embed(title="Sirk Bot", description="Hey there :wave: Seems like you mentioned me.\n\nMy prefixes are: `@Sirk ` and `^`\nIf you would like to see my commands type `[prefix]help`", color=0x2F3136)
        await message.channel.send(embed=embed)
    else:
        await bot.process_commands(message)
@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)
    if after.attachments and before.attachments:
        return


bot.loop.create_task(ainit())

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.load_extension("jishaku")

#16003
bot.run(token)
