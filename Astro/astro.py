import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

list1 = ['^', '<@!751447995270168586> ', 'astro ','Astro ']
bot = commands.Bot(command_prefix = list1)

#bot.remove_command('help')

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
    await ctx.send(f'{extension}' " loaded.")

@commands.is_owner()
@bot.command()
async def unload(ctx, extension):
    '''Unload a cog.'''
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension}' " unloaded.")

@commands.is_owner()
@bot.command()
async def reload(ctx, extension):
    '''Reload a cog.'''
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension}' " reloaded.")

for filename in os.listdir('./Astro/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.load_extension("jishaku")

#3549
bot.run(os.getenv('TOKEN'))
