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

import discord
from discord.ext import commands, menus
import os, io, json, psutil, collections, time, datetime, random, requests, asyncio, re, inspect
from datetime import datetime
import subprocess
from jishaku import codeblocks

class SourceMenu(menus.Menu):
    def __init__(self, source: str, **kwargs):
        super().__init__(delete_message_after=True, **kwargs)
        
    async def send_initial_message(self, ctx, channel: discord.TextChannel):
        return await channel.send(embed=discord.Embed(description=source,color=self.ctx.bot.color))
    
    @menus.button('❌')
    async def do_end(self, _):
        self.stop()

class dev(commands.Cog):
    '''Developer Commands'''
    def __init__(self, bot):
        self.bot = bot
        
    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner
        return True
        
    @commands.command()
    async def load(self, ctx, name: str):
        """Loads an extension. """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
        await ctx.send(f"📥 Loaded extension **`cogs/{name}.py`**")

    @commands.command(aliases=['r'])
    async def reload(self, ctx, name: str):
        """Reloads an extension. """

        try:
            self.bot.reload_extension(f"cogs.{name}")
            await ctx.message.add_reaction('🔁')

        except Exception as e:
            return await ctx.send(f"```py\n{e}```")

    @commands.command()
    async def unload(self, ctx, name: str):
        """Unloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
        await ctx.send(f"📤 Unloaded extension **`cogs/{name}.py`**")
    
    @commands.command(aliases=['ra'])
    async def reloadall(self, ctx):
        """Reloads all extensions. """
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    return await ctx.send(f"```py\n{e}```")

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        await ctx.message.add_reaction('🔁')

    @commands.command(aliases=['s'])
    async def sync(self, ctx):
        """Sync with GitHub"""
        out = subprocess.check_output("git pull", shell=True)
        await ctx.send(f"```{out.decode('utf-8')}```")

    @commands.command()
    async def leaveguildanddontchokeisirk(self, ctx):
        '''[Pain](https://canary.discord.com/channels/336642139381301249/381963689470984203/779527415307173909)'''
        embed=discord.Embed(title='Goodbye', color=self.bot.color)
        await ctx.send(embed=embed)
        await ctx.guild.leave()
    
    @commands.command()
    async def status(self, ctx, kwarg: int, *, status: str):
        '''Playing, Watching, Listening, Reset'''
        if kwarg == 1:
            await self.bot.change_presence(activity=discord.Game(name=status))
            await ctx.send(f'Changed status to  `Playing {status}`')
        elif kwarg == 2:
            activity = discord.Activity(
                name=status, type=discord.ActivityType.watching)
            await self.bot.change_presence(activity=activity)
            await ctx.send(f'Changed status to `Watching {status}`')
        elif kwarg == 3:
            activity = discord.Activity(
                name=status, type=discord.ActivityType.listening)
            await self.bot.change_presence(activity=activity)
            await ctx.send(f'Changed status to `Listening to {status}`')
        elif kwarg == 4:
            await self.bot.change_presence(status=discord.Status.online)
            await ctx.send(f'Reset Status')
        
    @commands.command()
    async def dm(self , ctx, user : discord.Member, *, content):
        '''Dm a Member'''
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(name=f"Sent from {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Message:", value=f'{content}')
        embed.set_footer(text=self.bot.footer)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/726779670514630667.png?v=1")
        await user.send(embed=embed)
        await ctx.send(f"<:comment:726779670514630667> Message sent to {user}")
        
    @commands.command(aliases = ["ss"])
    async def screenshot(self, ctx, url):
        '''Screenshot given website'''
        embed = discord.Embed(title = f"Screenshot of {url}", color=self.bot.color)
        async with self.bot.session.get(f'https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}') as r:
            res = await r.read()
        embed.set_image(url="attachment://ss.png")
        embed.set_footer(text=self.bot.footer)
        await ctx.send(file=discord.File(io.BytesIO(res), filename="ss.png"), embed=embed)
    
    @commands.command()
    async def say(self, ctx, *, content:str):
        '''Make the bot say something'''
        await ctx.send(content)
          
    @commands.command(aliases=['e'])
    async def eval(self, ctx, *, code: str):
        '''Evaluate code'''
        cog = self.bot.get_cog("Jishaku")
        res = codeblocks.codeblock_converter(code)
        await cog.jsk_python(ctx, argument=res)

    @commands.command()
    async def sudo(self, ctx, *, command:str):
        '''Sudo command'''
        cog = self.bot.get_cog("Jishaku")
        await cog.jsk_sudo(ctx, command_string=command)
        
    @commands.command()
    async def nick(self, ctx, *, name=None):
        if name is None:
            await ctx.guild.me.edit(nick=None)
            await ctx.send("Nickname reset to `Sirk`")
        else:
            try:
                await ctx.guild.me.edit(nick=name)
                await ctx.send(f"Successfully changed username to **{name}**")
            except discord.HTTPException as err:
                await ctx.send(f"```{err}```")
        
    @commands.command()
    async def cogs(self, ctx):
        s = ""
        for cog in self.bot.cogs.keys():
            s += f"\n {cog}"
        embed = discord.Embed(title = "Active Cogs:", description = f"```yaml\n{s}```", color=self.bot.color)
        embed.set_footer(text=self.bot.footer)
        await ctx.send(embed=embed)
      
    @commands.command(aliases=['bp'])
    async def botpurge(self, ctx, limit=50):
        channel = ctx.message.channel

        def is_me(m):
            return m.author == self.bot.user

        deleted = await channel.purge(limit=limit, check=is_me, bulk=False)
        await channel.send(f"I have deleted `{len(deleted)}` out of the `{limit}` requested messages.", delete_after=10)

    @commands.command()
    async def get_invite(self, ctx, id: int):
        guild = self.bot.get_guild(id)

        for channel in guild.text_channels:
            channels = [channel.id]

        picked = random.choice(channels)
        channel = self.bot.get_channel(picked)

        invite = await channel.create_invite(max_uses=1)

        await ctx.author.send(invite)

    @commands.command()
    async def reply(self, ctx, messageId, *, reply = None):
        if not reply: return await ctx.reply("You didn't provide a reply!")
        e = await ctx.fetch_message(messageId) 
        await e.reply(reply)
    
    @commands.command()
    async def sql(self, ctx, *, query):
        """Makes an sql SELECT query"""
        query = codeblocks.codeblock_converter(query)[1]
        if not query.lower().startswith("select"):
            data = await self.bot.db.execute(query)
            return await ctx.send(data)
        else:
            e = await self.bot.db.fetch(query)
            try:
                p = self.bot.utils.Simple(entries=e, per_page=10)
                await p.start(ctx)
            except menus.MenuError as f:
                await ctx.send(f)

    @commands.command(aliases=['logout'])
    async def shutdown(self, ctx):
        await ctx.send("Shutting Down")
        await self.bot.close()
        await self.bot.db.close()
        await self.bot.session.close()

    @commands.command(aliases=['src'])
    async def source(self, ctx, cmd: str):
        cmd = self.bot.get_command(cmd)
        src = inspect.getsource(cmd.callback)
        await SourceMenu(src).start(ctx)
            
    @commands.group(invoke_without_command=True)
    async def todo(self, ctx):
        """Todo Commands"""
        s = await self.bot.db.fetch("SELECT * FROM todo")
        p = self.bot.utils.Simple(entries=[x["todo"] for x in s], per_page=10)
        await p.start(ctx)
            
    @todo.command()
    async def add(self, ctx, *, thing:str):
        '''Add something to the todo list'''
        try:
            await self.bot.db.execute("INSERT INTO todo VALUES ($1)", thing)
            await ctx.send(f'Added {thing} to your todo list!')
        except Exception as e:
            return await ctx.send(e)

    @todo.command(aliases=['remove'])
    async def delete(self, ctx, *, thing:str):
        '''Delete an item from your todo list'''
        try:
            await self.bot.db.execute("DELETE FROM todo WHERE todo = $1", thing)
            await ctx.send(f'Removed {thing} from your todo list!')
        except Exception as e:
            return await ctx.send(e)

    @commands.command()
    @commands.is_owner()
    async def give(self, ctx, user: discord.User, amount: int):
        '''
        Give someone money
        '''
        user = self.bot.get_user(user.id)
        a = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", user.id)
        if not a:
            await ctx.send(f"{user.name} doesn't have a bank account!")
        else:
            await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", a['cashbalance']+amount, user.id)
            await ctx.send(f'Gave **{user.name}** `{amount}`.')

    @commands.command()
    @commands.is_owner()
    async def take(self, ctx, user: discord.User, amount: int):
        '''
        Take money from someone
        '''
        user = self.bot.get_user(user.id)
        a = await self.bot.db.fetchrow("SELECT * FROM ECONOMY WHERE userid = $1", user.id)
        if not a:
            await ctx.send(f"{user.name} doesn't have a bank account!")
        else:
            await self.bot.db.execute("UPDATE economy SET cashbalance = $1 WHERE userId = $2", a['cashbalance']-amount, user.id)
            await ctx.send(f'Took `{amount}` from **{user.name}**')

def setup(bot):
    bot.add_cog(dev(bot))
