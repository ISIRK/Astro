import discord, os, io, json, psutil, collections, time, datetime, random, requests, asyncio, re, inspect, subprocess
from discord.ext import commands, menus
from datetime import datetime
from jishaku import codeblocks

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
        await ctx.remove(f"```{out.decode('utf-8')}```")

    @commands.command()
    async def leaveguild(self, ctx, id: int):
        '''[Pain](https://canary.discord.com/channels/336642139381301249/381963689470984203/779527415307173909)'''
        guild = self.bot.get_guild(id) or ctx.guild
        await guild.leave()

    @commands.command()
    async def inv(self, ctx, id: int):
        guild = self.bot.get_guild(id)

        for channel in guild.text_channels:
            channels = [channel.id]

        picked = random.choice(channels)
        channel = self.bot.get_channel(picked)

        invite = await channel.create_invite(max_uses=1)

        await ctx.author.send(invite)
    
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
        embed = discord.Embed(color=self.bot.color)
        async with ctx.typing():
            async with self.bot.session.get(f'https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}') as r:
                res = await r.read()
            embed.set_image(url="attachment://ss.png")
            embed.set_footer(text=self.bot.footer)
            await ctx.remove(file=discord.File(io.BytesIO(res), filename="ss.png"), embed=embed)
    
    @commands.command()
    async def say(self, ctx, channel: int, *, content:str):
        '''Make the bot say something'''
        c = ctx.channel if channel == 0 else ctx.guild.get_channel(channel)
        await c.send(content)
          
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
        embed = discord.Embed(title = "Active Cogs:", description = '\n'.join([cog for cog in self.bot.cogs]), color=self.bot.color).set_footer(text=self.bot.footer)
        await ctx.send(embed=embed)
      
    @commands.command(aliases=['bp'])
    async def botpurge(self, ctx, limit=50):
        channel = ctx.message.channel

        def is_me(m):
            return m.author == self.bot.user

        deleted = await channel.purge(limit=limit+1, check=is_me, bulk=False)

    @commands.command()
    async def edit(self, ctx, id: int, *, content):
        m = await ctx.channel.fetch_message(id)
        await m.edit(content=content)

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
                p = self.bot.utils.SimpleMenu(entries=e, per_page=10)
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
        await ctx.remove(embed=discord.Embed(description=f"```py\n{inspect.getsource(self.bot.get_command(cmd).callback)}```", color=self.bot.color))

    @commands.command()
    async def remind(self, ctx, time: int, *, thing: str):
        await asyncio.sleep(time)
        await ctx.send(f'{ctx.author.mention} --> **{thing}**')
            
    @commands.group(invoke_without_command=True)
    async def todo(self, ctx):
        """Todo Commands"""
        s = await self.bot.db.fetch("SELECT * FROM todo WHERE id = $1", ctx.author.id)
        if s:
            p = self.bot.utils.SimpleMenu(entries=s['things'], per_page=10)
            await p.start(ctx)
        else:
            await self.bot.db.execute("INSERT INTO todo(id) VALUES ($1)", ctx.author.id)
            await ctx.send("Registered a todo list for you.")
            
    @todo.command()
    async def add(self, ctx, *, thing:str):
        '''Add something to the todo list'''
        s = await self.bot.db.fetch("SELECT * FROM todo WHERE id = $1", ctx.author.id)
        if s:
            try:
                await self.bot.db.execute("INSERT INTO todo(things) VALUES ($1) WHERE id = $2", s['things'].append(thing), ctx.author.id)
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
