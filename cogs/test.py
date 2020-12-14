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

import discord, json, aiohttp, random, asyncio
import subprocess as sp
from discord.ext import commands, menus

tools = "json/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

# ext-menus paginator
class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        return await channel.send(f'Hello {ctx.author}')

    @menus.button('\N{THUMBS UP SIGN}')
    async def on_thumbs_up(self, payload):
        await self.message.edit(content=f'Thanks {self.ctx.author}!')

    @menus.button('\N{THUMBS DOWN SIGN}')
    async def on_thumbs_down(self, payload):
        await self.message.edit(content=f"That's not nice {self.ctx.author}...")

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()
        
# ext-menus Embed paginator
class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, embed):
        return embed
    
class test(commands.Cog, command_attrs=dict(hidden=True)):
    '''Testing Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
            
    @commands.command()
    async def menu(self, ctx):
        m = MyMenu()
        await m.start(ctx)
    
    @commands.command()
    async def emenu(self, ctx):
        embeds = [
            discord.Embed(title="Embed"),
            discord.Embed(title="Another embed"),
            discord.Embed(title="Some other embed")
        ]
        menu = menus.MenuPages(EmbedPageSource(embeds, per_page=1))
        await menu.start(ctx)

    @commands.command()
    async def shakey(self, ctx):
        '''Shakespear'''
        headers = {'content-type': 'application/json'}
        async with self.session.get("https://www.foaas.com/shakespeare/PB/isirk", headers=headers) as r:
            resp = await r.json()
        await ctx.send(resp['message'])

    @commands.command()
    async def premium(self, ctx):
        user = ctx.author
        with open('json/premium.txt') as f:
            if f'{user.id}' in f.read():
                await ctx.send("Member has premium.")
            else:
                await ctx.send('Member does not have premium')
        
    @commands.is_owner()
    @commands.command()
    async def simon(self, ctx):
        """Start a game of Simon."""
        await ctx.send(
            "Starting game...\n**RULES:**\n```1. When you are ready for the sequence, click the green checkmark.\n2. Watch the sequence carefully, then repeat it back into chat.  For example, if the 1 then the 2 changed, I would type 12.\n3. You are given 10 seconds to repeat the sequence.\n4. When waiting for confirmation for next sequence, click the green check within 5 minutes of the bot being ready.\n5. Answer as soon as you can once the bot adds the stop watch emoji.```"
        )
        board = [[1, 2], [3, 4]]
        level = [1, 4]
        points = 0
        message = await ctx.send("```" + self.print_board(board) + "```")
        await message.add_reaction("\u2705")
        await message.add_reaction("\u274C")
        await ctx.send("Click the Green Check Reaction when you are ready for the sequence.")

        def check(reaction, user):
            return (
                (user.id == ctx.author.id)
                and (str(reaction.emoji) in ["\u2705", "\u274C"])
                and (reaction.message.id == message.id)
            )

        randoms = []
        for x in range(4):
            randoms.append(random.randint(1, 4))

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=300.0
                )
            except asyncio.TimeoutError:
                await message.delete()
                await ctx.send(
                    f"Game has ended due to no response for starting the next sequence.  You got {points} sequence{'s' if points != 1 else ''} correct!"
                )
                return
            else:
                if str(reaction.emoji) == "\u274C":
                    await message.delete()
                    await ctx.send(
                        f"Game has ended due to no response.  You got {points} sequence{'s' if points != 1 else ''} correct!"
                    )
                    return
                await message.remove_reaction("\u2705", self.bot.user)
                await message.remove_reaction("\u274C", self.bot.user)
                try:
                    await message.remove_reaction("\u2705", ctx.author)
                except discord.errors.Forbidden:
                    pass
                await message.add_reaction("\u26A0")
                for x in randoms:
                    await asyncio.sleep(1)
                    if x == 1:
                        board[0][0] = "-"
                        await message.edit(content="```" + self.print_board(board) + "```")
                        await asyncio.sleep(level[0])
                        board[0][0] = 1
                    elif x == 2:
                        board[0][1] = "-"
                        await message.edit(content="```" + self.print_board(board) + "```")
                        await asyncio.sleep(level[0])
                        board[0][1] = 2
                    elif x == 3:
                        board[1][0] = "-"
                        await message.edit(content="```" + self.print_board(board) + "```")
                        await asyncio.sleep(level[0])
                        board[1][0] = 3
                    elif x == 4:
                        board[1][1] = "-"
                        await message.edit(content="```" + self.print_board(board) + "```")
                        await asyncio.sleep(level[0])
                        board[1][1] = 4
                    await message.edit(content="```" + self.print_board(board) + "```")
                await message.remove_reaction("\u26A0", self.bot.user)
                answer = "".join(list(map(str, randoms)))
                await message.add_reaction("\u23F1")

                def check_t(m):
                    return (m.author.id == ctx.author.id) and (m.content.isdigit())

                try:
                    user_answer = await self.bot.wait_for("message", check=check_t, timeout=10.0)
                except asyncio.TimeoutError:
                    await ctx.send(
                        f"Sorry {ctx.author.mention}!  You took too long to answer.  You got {points} sequence{'s' if points != 1 else ''} correct!"
                    )
                    await message.remove_reaction("\u23F1", self.bot.user)
                    return
                else:
                    try:
                        await user_answer.delete()
                    except discord.errors.Forbidden:
                        pass
                    await message.remove_reaction("\u23F1", self.bot.user)
                    if str(user_answer.content) == str(answer):
                        await message.add_reaction("\U0001F44D")
                    else:
                        await message.add_reaction("\U0001F6AB")
                        await ctx.send(
                            f"Sorry, but that was the incorrect pattern.  The pattern was {answer}.  You got {points} sequence{'s' if points != 1 else ''} correct!"
                        )
                        return
                    another_message = await ctx.send("Sequence was correct.")
                    points += 1
                    await asyncio.sleep(3)
                    await message.remove_reaction("\U0001F44D", self.bot.user)
                    await message.add_reaction("\u2705")
                    await message.add_reaction("\u274C")
                    await another_message.delete()
                level[0] *= 0.90
                randoms.append(random.randint(1, 4))

    def print_board(self, board):
        col_width = max(len(str(word)) for row in board for word in row) + 2  # padding
        whole_thing = ""
        for row in board:
            whole_thing += "".join(str(word).ljust(col_width) for word in row) + "\n"
        return whole_thing

def setup(bot):
    bot.add_cog(test(bot))
