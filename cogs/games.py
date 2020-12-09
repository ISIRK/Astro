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

import discord, random, json, time, asyncio, aiohttp
from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType
import asyncio
import random
from copy import deepcopy as dc

tools = "json/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)


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
    
class games(commands.Cog):
    '''Game Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        
    @commands.cooldown(1,3,BucketType.user)   
    @commands.command(aliases=['cb'])
    async def chatbot(self, ctx, *, message):
        '''Talk to chatbot'''
        async with self.session.get(f"http://bruhapi.xyz/cb/{message}") as r:
            resp = await r.json()
        await ctx.send(resp['res'])
        
    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def dice(self, ctx):
        '''Roll a dice'''
        dice = ['1', '2', '3', '4', '5', '6', 'off the table...\n*You Found The Mystery!*']
        embed = discord.Embed(title="Dice", description=f'The Dice Rolled {random.choice(dice)}', color=color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/758138226874908705/766312838910181421/unknown.png")
        embed.set_footer(text=footer)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,3,BucketType.user)
    async def quiz(self, ctx):
        '''Take a Chritmas quiz'''
        qa = {
            "`Was King William I of England was crowned on Christmas Day.(Yes/No)`": "YES",
            "`When is Christmas?`": "DECEMBER 25",
            "`Who delivers toys?`" : "SANTA"
        }
        total_questions = len(qa)
        start_time = time.time()

        def check(message):
            return ctx.author == message.author and ctx.channel == message.channel

        for i, (question, answer) in enumerate(qa.items()):
            content = ""
            append = "Type your answer below"

            if i == 0:
                content += "Quiz Started!\n"
            else:
                content += "Correct!\n"
            content += (f"**Question {i+1})** {question}\n"
                        f"{append}")
            await ctx.send(content)

            try:
                message = await self.bot.wait_for("message", timeout=45.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Timeout Error")

            if message.content.upper() != answer:
                return await ctx.send(f"Incorrect.\nIf you would like to try again type `{ctx.prefix}quiz`")
        time_taken = time.time()- start_time
        await ctx.send(f"Correct!\nYou took **{time_taken:,.2f} seconds!**")

    
    @commands.cooldown(1,3,BucketType.user)
    @commands.command()
    async def rps(self, ctx):
        """Rock paper scissors, either play against the bot or against a user"""
        choices = ["\U0001f4f0", "\U0001faa8", "\U00002702"]
        s = m = await ctx.send(embed = discord.Embed(title = f"Rock, Paper, Scissors.", description = f" {str(ctx.author)} Choose your weapon!", color=color))
        for i in choices:
            await m.add_reaction(i)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in choices

        try:
            reaction = await self.bot.wait_for('reaction_add', timeout = 30.0, check = check)
            reaction = reaction[0].emoji
            botChoice = random.choice(choices)
            result = rps_winner(reaction, botChoice)

            await s.edit(embed= discord.Embed(title =result , description = f"I picked {botChoice} and you picked {reaction}.", color=color))

        except asyncio.TimeoutError: return await ctx.send("You didn't add a reaction in time!")
        
    @commands.cooldown(1,30,BucketType.channel)
    @commands.command()
    async def twenty(self, ctx):
        """Starts a 2048 game inside of Discord."""
        ## Made by NeuroAssassin [https://github.com/NeuroAssassin/Toxic-Cogs/blob/master/twenty/twenty.py]
        board = [
            ["_", "_", "_", "_"],
            ["_", "_", "_", "_"],
            ["_", "_", "_", "_"],
            ["_", "_", "_", 2],
        ]
        score = 0
        total = 0
        await ctx.send(
            "Starting game...\nIf a reaction is not received every 5 minutes, the game will time out."
        )
        message = await ctx.send(f"Score: **{score}**```{self.print_board(board)}```")
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
                    "reaction_add", check=check, timeout=300.0
                )
            except asyncio.TimeoutError:
                await ctx.send("Ending game")
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
                    await ctx.send("Ending game")
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
                await message.edit(content=f"Score: **{score}**```{self.print_board(board)}```")

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

def setup(bot):
    bot.add_cog(games(bot))
