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

import discord, random, json, time, asyncio, random
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType
from copy import deepcopy as dc
import async_cleverbot as ac

config = "tools/config.json"
with open(config) as f:
    data = json.load(f)
cb = data['CLEVERBOT']

cleverbot = ac.Cleverbot(cb)

def rps_winner(userOneChoice, userTwoChoice):
    if userOneChoice == "\U0001faa8":
        if userTwoChoice == "\U00002702": return "You won!"
        if userTwoChoice == "\U0001faa8": return "Tie!"
        if userTwoChoice == "\U0001f4f0": return "I won!"
    elif userOneChoice == "\U00002702":
        if userTwoChoice == "\U00002702": return "Tie!"
        if userTwoChoice == "\U0001faa8": return "I won!"
        if userTwoChoice == "\U0001f4f0": return "You Won!"
    elif userOneChoice == "\U0001f4f0":
        if userTwoChoice == "\U00002702": return "I won!"
        if userTwoChoice == "\U0001faa8": return "You won!"
        if userTwoChoice == "\U0001f4f0": return "Tie!"
    else: return "error"

class BasketballMenu(menus.Menu):
    def __init__(self, **kwargs):
        super().__init__(delete_message_after=True, **kwargs)
        self.score = 0
        self.footer = 'Use the reactions below to try and score'
        
    async def send_initial_message(self, ctx, channel: discord.TextChannel):
        return await channel.send(embed=discord.Embed(title='Basketball!', description='Play basketball against an AI!\n\nUse the reactions below to play:\n\n🗑️ = Take a shot\n🏀 = Pass the ball\n⛹️ = Drive to get a layup\n📟 = See the score\n❓ = See this message\n❌ = Stop the game\n\n**Note this command is a work in progress.**',color=self.ctx.bot.color))
    
    @menus.button('🗑️')
    async def do_shot(self, _):
        if self.score >= 21:
            await self.message.edit(embed=discord.Embed(title='You reached 21!', color=self.ctx.bot.color))
        else:
            lucky = random.choice([True, False])
            if lucky:
                three = random.choice([True, False])
                if three:
                    self.score += 3
                    d = 'You swished a three! Good job. +3 to your score.'
                else:
                    d = 'You made a jump shot! +2 to your score.'
                    self.score += 2
            else:
                d = 'You missed.'
                pass
            embed = discord.Embed(title='Shot...', description=d, color=self.ctx.bot.color)
            embed.set_footer(text=self.footer)
            await self.message.edit(embed = embed)

    @menus.button('🏀')
    async def do_pass(self, _):
        p = random.choice(['Bob', 'Joe', 'Tim', 'Jordan', 'Jokic'])
        lucky = random.choice([True, False])
        if lucky:
            d = f'Nice give and go! You passed the ball to **{p}** and they scored a layup. +2 to your score.'
        else:
            d = f'You passed the ball to **{p}** but they dropped it.'
        embed = discord.Embed(title='Pass...', description=d, color=self.ctx.bot.color)
        embed.set_footer(text=self.footer)
        await self.message.edit(embed = embed)

    @menus.button('⛹️')
    async def do_drive(self, _):
        embed = discord.Embed(title='Drive...', color=self.ctx.bot.color)
        embed.set_footer(text=self.footer)
        await self.message.edit(embed = embed)

    @menus.button('📟')
    async def do_score(self, _):
        embed = discord.Embed(title='Current Score', description=f'**{self.ctx.author.name}** - {self.score}', color=self.ctx.bot.color)
        embed.set_footer(text=self.footer)
        await self.message.edit(embed = embed)

    @menus.button('❓')
    async def do_help(self, _):
        await self.message.edit(embed=discord.Embed(title='Basketball!', description='Play basketball against an AI!\n\nUse the reactions below to play:\n\n🗑️ = Take a shot\n🏀 = Pass the ball\n⛹️ = Drive to get a layup\n📟 = See the score\n❓ = See this message\n❌ = Stop the game\n\n**Note this command is a work in progress.**',color=self.ctx.bot.color))

    @menus.button('❌')
    async def do_end(self, _):
        self.stop()
    
class games(commands.Cog):
    '''Game Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def basketball(self, ctx):
        '''Play basketball in a D&D style'''
        await BasketballMenu().start(ctx)
        
    @commands.max_concurrency(1, per=BucketType.channel, wait=False)
    @commands.command(aliases=['cb'])
    async def chatbot(self, ctx):
        '''Talk to chatbot'''
        talk = True
        await ctx.send('Chatbot Started!\nType `cancel` to end.')
        while talk is True:
            try:
                m = await self.bot.wait_for('message', timeout=30, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
            except asyncio.TimeoutError:
                await ctx.send('Timeout Error')
                talk = False
            else:
                if m.content.lower() == "cancel":
                    talk = False
                    await ctx.send('Chatbot Session Ended.')
                else:
                    async with ctx.channel.typing():
                        response = await cleverbot.ask(m.content) # Ask a question, returns async_cleverbot.cleverbot.Response
                        await ctx.send(response.text)
        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def dice(self, ctx):
        '''Roll a dice'''
        dice = ['1', '2', '3', '4', '5', '6', 'off the table...\n*You Found The Mystery!*']
        embed = discord.Embed(title="Dice", description=f'The Dice Rolled {random.choice(dice)}', color=self.bot.color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758138226874908705/766312838910181421/unknown.png")
        embed.set_footer(text=self.bot.footer)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.cooldown(1,3,BucketType.user)
    @commands.command()
    async def rps(self, ctx):
        """Rock paper scissors, either play against the bot or against a user"""
        choices = ["\U0001f4f0", "\U0001faa8", "\U00002702"]
        s = m = await ctx.send(embed = discord.Embed(title = f"Rock, Paper, Scissors.", description = f" {str(ctx.author)} Choose your weapon!", color=self.bot.color))
        for i in choices:
            await m.add_reaction(i)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in choices

        try:
            reaction = await self.bot.wait_for('reaction_add', timeout = 30.0, check = check)
            reaction = reaction[0].emoji
            botChoice = random.choice(choices)
            result = rps_winner(reaction, botChoice)

            await s.edit(embed= discord.Embed(title =result , description = f"I picked {botChoice} and you picked {reaction}.", color=self.bot.color))

        except asyncio.TimeoutError: return await ctx.send("You didn't add a reaction in time!")

    @commands.max_concurrency(1, per=commands.BucketType.channel)
    @commands.command() #aliases=["c"]
    async def cookie(self, ctx):
        """
        Yum yum.
        """
        cookie = "🍪"
        embed = discord.Embed(description=f"Fastest person to eat the {cookie} wins!", colour=self.bot.color)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(4)
        for i in reversed(range(1, 4)):
            await message.edit(embed=discord.Embed(description=str(i), colour=self.bot.color))
            await asyncio.sleep(1)
        await asyncio.sleep(random.randint(0, 3))
        await message.edit(embed=discord.Embed(description="Eat the cookie!", colour=self.bot.color))
        await message.add_reaction(cookie)
        start = time.perf_counter()
        try:
            _, user = await ctx.bot.wait_for(
                "reaction_add",
                check=lambda _reaction, user: _reaction.message.guild == ctx.guild
                and _reaction.message.channel == ctx.message.channel
                and _reaction.message == message and str(_reaction.emoji) == cookie and user != ctx.bot.user
                and not user.bot,
                timeout=60,)
        except asyncio.TimeoutError:
            return await message.edit(embed=discord.Embed(description="No one ate the cookie...",
                                                          colour=self.bot.color))
        end = time.perf_counter()
        await message.edit(embed=discord.Embed(description=f"**{user}** ate the cookie in `{end - start:.3f}` seconds!", colour=self.bot.color))
        
    @commands.max_concurrency(1, per=BucketType.guild, wait=False)
    @commands.command(aliases=['2048', '24'])
    async def twenty(self, ctx):
        """Starts a 2048 game inside of Discord.
        Join the support server to post your score!"""
        board = [
            ["_", "_", "_", "_"],
            ["_", "_", "_", "_"],
            ["_", "_", "_", "_"],
            ["_", "_", "_", 2],
        ]
        score = 0
        total = 0
        embed=discord.Embed(title="2048", description=f"If a reaction is not received every 2 minutes, the game will time out.\n\n```{self.print_board(board)}```", color=self.bot.color)
        message = await ctx.send(embed=embed)
        await message.add_reaction("\u2B06")
        await message.add_reaction("\u2B07")
        await message.add_reaction("\u2B05")
        await message.add_reaction("\u27A1")
        await message.add_reaction("\u274C")

        def check(reaction, user):
            return (
                (user.id == ctx.author.id)
                and (str(reaction.emoji) in ["\u2B06", "\u2B07", "\u2B05", "\u27A1", "\u274C"])
                and (reaction.message.id == message.id)
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=120.0
                )
            except asyncio.TimeoutError:
                await ctx.send(f"Ending game.\nYour score was **{score}**")
                await message.delete()
                return
            else:
                try:
                    await message.remove_reaction(str(reaction.emoji), ctx.author)
                except discord.errors.Forbidden:
                    pass
                if str(reaction.emoji) == "\u2B06":
                    msg, nb, total = self.execute_move("up", board)
                elif str(reaction.emoji) == "\u2B07":
                    msg, nb, total = self.execute_move("down", board)
                elif str(reaction.emoji) == "\u2B05":
                    msg, nb, total = self.execute_move("left", board)
                elif str(reaction.emoji) == "\u27A1":
                    msg, nb, total = self.execute_move("right", board)
                elif str(reaction.emoji) == "\u274C":
                    await ctx.send(f"Ending game.\nYour score was **{score}**")
                    await message.delete()
                    return
                score += total
                if msg == "Lost":
                    await ctx.send(
                        f"Oh no!  It appears you have lost {ctx.author.mention}.  You finished with a score of {score}!"
                    )
                    await message.delete()
                    return
                board = nb
                sem=discord.Embed(title=f"Score: **{score}**", description=f"```{self.print_board(board)}```", color=self.bot.color)
                'await message.edit(content=f"Score: **{score}**```{self.print_board(board)}```")'
                await message.edit(embed=sem)

    def print_board(self, board):
        col_width = max(len(str(word)) for row in board for word in row) + 2  # padding
        whole_thing = ""
        for row in board:
            whole_thing += "".join(str(word).ljust(col_width) for word in row) + "\n"
        return whole_thing

    def execute_move(self, move, pboard):
        board = dc(pboard)
        total = 0
        if move.lower() == "left":
            nb, total = self.check_left(board)
            for x in range(len(nb)):
                while nb[x][0] == "_" and (nb[x][1] != "_" or nb[x][2] != "_" or nb[x][3] != "_"):
                    nb[x][0] = nb[x][1]
                    nb[x][1] = nb[x][2]
                    nb[x][2] = nb[x][3]
                    nb[x][3] = "_"
                while nb[x][1] == "_" and (nb[x][2] != "_" or nb[x][3] != "_"):
                    nb[x][1] = nb[x][2]
                    nb[x][2] = nb[x][3]
                    nb[x][3] = "_"
                while nb[x][2] == "_" and (nb[x][3] != "_"):
                    nb[x][2] = nb[x][3]
                    nb[x][3] = "_"
        if move.lower() == "right":
            nb, total = self.check_right(board)
            for x in range(len(nb)):
                while nb[x][3] == "_" and (nb[x][2] != "_" or nb[x][1] != "_" or nb[x][0] != "_"):
                    nb[x][3] = nb[x][2]
                    nb[x][2] = nb[x][1]
                    nb[x][1] = nb[x][0]
                    nb[x][0] = "_"
                while nb[x][2] == "_" and (nb[x][1] != "_" or nb[x][0] != "_"):
                    nb[x][2] = nb[x][1]
                    nb[x][1] = nb[x][0]
                    nb[x][0] = "_"
                while nb[x][1] == "_" and (nb[x][0] != "_"):
                    nb[x][1] = nb[x][0]
                    nb[x][0] = "_"
        if move.lower() == "down":
            nb = self.columize(board)
            nb, total = self.check_down(nb)
            for x in range(len(nb)):
                while nb[x][0] == "_" and (nb[x][1] != "_" or nb[x][2] != "_" or nb[x][3] != "_"):
                    nb[x][0] = nb[x][1]
                    nb[x][1] = nb[x][2]
                    nb[x][2] = nb[x][3]
                    nb[x][3] = "_"
                while nb[x][1] == "_" and (nb[x][2] != "_" or nb[x][3] != "_"):
                    nb[x][1] = nb[x][2]
                    nb[x][2] = nb[x][3]
                    nb[x][3] = "_"
                while nb[x][2] == "_" and (nb[x][3] != "_"):
                    nb[x][2] = nb[x][3]
                    nb[x][3] = "_"
            nb = self.rowize(nb)
        if move.lower() == "up":
            nb = self.columize(board)
            nb, total = self.check_up(nb)
            for x in range(len(nb)):
                while nb[x][3] == "_" and (nb[x][2] != "_" or nb[x][1] != "_" or nb[x][0] != "_"):
                    nb[x][3] = nb[x][2]
                    nb[x][2] = nb[x][1]
                    nb[x][1] = nb[x][0]
                    nb[x][0] = "_"
                while nb[x][2] == "_" and (nb[x][1] != "_" or nb[x][0] != "_"):
                    nb[x][2] = nb[x][1]
                    nb[x][1] = nb[x][0]
                    nb[x][0] = "_"
                while nb[x][1] == "_" and (nb[x][0] != "_"):
                    nb[x][1] = nb[x][0]
                    nb[x][0] = "_"
            nb = self.rowize(nb)
        if (
            nb != pboard
        ):  # So the user doesn't make a move that doesn't change anything, and just add a number
            some_message, nb = self.add_number(nb)
        else:
            some_message = ""
        if some_message.startswith("Lost"):
            return "Lost", nb, total
        else:
            return "", nb, total

    def add_number(self, board):
        try:
            row = random.randint(0, 3)
        except RecursionError:
            return "Lost", board
        if "_" in board[row]:
            number_of_zeroes = board[row].count("_")
            if number_of_zeroes == 1:
                column = board[row].index("_")
            else:
                column = random.randint(0, 3)
                while board[row][column] != "_":
                    column = random.randint(0, 3)
        else:
            result, board = self.add_number(board)
            return result, board
        joining = random.randint(0, 100)
        if joining < 85:
            joining = 2
        else:
            joining = 4
        board[row][column] = joining
        return "", board

    def columize(self, board):
        new_board = [[], [], [], []]
        # Make first column
        new_board[0].append(board[3][0])
        new_board[0].append(board[2][0])
        new_board[0].append(board[1][0])
        new_board[0].append(board[0][0])
        # Make second column
        new_board[1].append(board[3][1])
        new_board[1].append(board[2][1])
        new_board[1].append(board[1][1])
        new_board[1].append(board[0][1])
        # Make third column
        new_board[2].append(board[3][2])
        new_board[2].append(board[2][2])
        new_board[2].append(board[1][2])
        new_board[2].append(board[0][2])
        # Make fourth column
        new_board[3].append(board[3][3])
        new_board[3].append(board[2][3])
        new_board[3].append(board[1][3])
        new_board[3].append(board[0][3])
        board = new_board
        return board

    def rowize(self, board):
        new_board = [[], [], [], []]
        # Make first row
        new_board[0].append(board[0][3])
        new_board[0].append(board[1][3])
        new_board[0].append(board[2][3])
        new_board[0].append(board[3][3])
        # Make second row
        new_board[1].append(board[0][2])
        new_board[1].append(board[1][2])
        new_board[1].append(board[2][2])
        new_board[1].append(board[3][2])
        # Make third row
        new_board[2].append(board[0][1])
        new_board[2].append(board[1][1])
        new_board[2].append(board[2][1])
        new_board[2].append(board[3][1])
        # Make fourth row
        new_board[3].append(board[0][0])
        new_board[3].append(board[1][0])
        new_board[3].append(board[2][0])
        new_board[3].append(board[3][0])
        board = new_board
        return board

    def check_left(self, board):
        total = 0
        for x in range(len(board)):
            for y in range(len(board[x])):
                try:
                    if board[x][y + 1] != "_":
                        if board[x][y] == board[x][y + 1]:
                            board[x][y] = board[x][y] + board[x][y + 1]
                            total += board[x][y]
                            board[x][y + 1] = "_"
                    elif board[x][y + 2] != "_":
                        if board[x][y] == board[x][y + 2]:
                            board[x][y] = board[x][y] + board[x][y + 2]
                            total += board[x][y]
                            board[x][y + 2] = "_"
                    elif board[x][y + 3] != "_":
                        if board[x][y] == board[x][y + 3]:
                            board[x][y] = board[x][y] + board[x][y + 3]
                            total += board[x][y]
                            board[x][y + 3] = "_"
                except IndexError:
                    pass
        return board, total

    def check_right(self, board):
        total = 0
        for x in range(len(board)):
            board[x].reverse()
            for y in range(len(board[x])):
                try:
                    if board[x][y + 1] != "_":
                        if board[x][y] == board[x][y + 1]:
                            board[x][y] = board[x][y] + board[x][y + 1]
                            total += board[x][y]
                            board[x][y + 1] = "_"
                    elif board[x][y + 2] != "_":
                        if board[x][y] == board[x][y + 2]:
                            board[x][y] = board[x][y] + board[x][y + 2]
                            total += board[x][y]
                            board[x][y + 2] = "_"
                    elif board[x][y + 3] != "_":
                        if board[x][y] == board[x][y + 3]:
                            board[x][y] = board[x][y] + board[x][y + 3]
                            total += board[x][y]
                            board[x][y + 3] = "_"
                except IndexError:
                    pass
            board[x].reverse()
        return board, total

    def check_up(self, board):
        total = 0
        for x in range(len(board)):
            board[x].reverse()
            for y in range(len(board[x])):
                try:
                    if board[x][y + 1] != "_":
                        if board[x][y] == board[x][y + 1]:
                            board[x][y] = board[x][y] + board[x][y + 1]
                            total += board[x][y]
                            board[x][y + 1] = "_"
                    elif board[x][y + 2] != "_":
                        if board[x][y] == board[x][y + 2]:
                            board[x][y] = board[x][y] + board[x][y + 2]
                            total += board[x][y]
                            board[x][y + 2] = "_"
                    elif board[x][y + 3] != "_":
                        if board[x][y] == board[x][y + 3]:
                            board[x][y] = board[x][y] + board[x][y + 3]
                            total += board[x][y]
                            board[x][y + 3] = "_"
                except IndexError:
                    pass
            board[x].reverse()
        return board, total

    def check_down(self, board):
        total = 0
        for x in range(len(board)):
            for y in range(len(board[x])):
                try:
                    if board[x][y + 1] != "_":
                        if board[x][y] == board[x][y + 1]:
                            board[x][y] = board[x][y] + board[x][y + 1]
                            total += board[x][y]
                            board[x][y + 1] = "_"
                    elif board[x][y + 2] != "_":
                        if board[x][y] == board[x][y + 2]:
                            board[x][y] = board[x][y] + board[x][y + 2]
                            total += board[x][y]
                            board[x][y + 2] = "_"
                    elif board[x][y + 3] != "_":
                        if board[x][y] == board[x][y + 3]:
                            board[x][y] = board[x][y] + board[x][y + 3]
                            total += board[x][y]
                            board[x][y + 3] = "_"
                except IndexError:
                    pass
        return board, total

    @commands.max_concurrency(1, per=BucketType.guild, wait=False)
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
    bot.add_cog(games(bot))
