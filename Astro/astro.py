import os

import discord
from discord.ext import commands
import json

from disputils.pagination import BotEmbedPaginator

##CONFIG
tokenFile = "/home/pi/Astro/Astro/.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data['TOKEN']
prefixes = data['PREFIX']

bot = commands.Bot(command_prefix = prefixes)
bot.owner_ids = {542405601255489537}
bot.remove_command('help')


os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

# also 
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"


@bot.event
async def on_ready():
    print('{0.user} is up and running'.format(bot))
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

@commands.is_owner()
@bot.command()
async def load(ctx, extension):
    '''Load a cog.'''
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension}' " loaded")

@commands.is_owner()
@bot.command()
async def unload(ctx, extension):
    '''Unload a cog.'''
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension}' " unloaded")

@commands.is_owner()
@bot.command()
async def reload(ctx, extension):
    '''Reload a cog.'''
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f':repeat: {extension}' " reloaded")

for filename in os.listdir('./Astro/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.load_extension("jishaku")

#19889
bot.run(token)