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

##CONFIG
tokenFile = "tools/config.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data['TOKEN']

prefixFile = "tools/tools.json"
with open(prefixFile) as f:
    data = json.load(f)
prefixes = data['PREFIXES']

intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("^"), intents=intents, allowed_mentions=discord.AllowedMentions(users=True, roles=False, everyone=False))
# Might Wanna look at this: command_prefix=commands.when_mentioned_or(prefixes)

bot.start_time = datetime.utcnow()

bot.owner_ids = {542405601255489537}
#bot.remove_command('help')

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

# also
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"


@bot.event
async def on_ready():
    print('{0.user} is up and running'.format(bot))
    # await bot.change_presence(status=discord.Status.idle)
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.content.endswith('<@!751447995270168586>'):
        embed = discord.Embed(title="Sirk Bot", description="Hey there :wave: Seems like you mentioned me.\n\nMy prefixes are: `@Sirk ` and `^`\nIf you would like to see my commands type `[prefix]help`", color=0x2F3136)
        await message.channel.send(embed=embed)
    if message.content.endswith('<@751447995270168586>'):
        embed = discord.Embed(title="Sirk Bot", description="Hey there :wave: Seems like you mentioned me.\n\nMy prefixes are: `@Sirk ` and `^`\nIf you would like to see my commands type `[prefix]help`", color=0x2F3136)
        await message.channel.send(embed=embed)

@loop(seconds=0)
async def status_changer():
    await asyncio.sleep(15)
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"" + str(guild_count) + f" servers | " + str(users) + " users"))
	await asyncio.sleep(60)
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"^help"))
	await asyncio.sleep(45)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.load_extension("jishaku")

#16003
bot.run(token)
