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

import dbl
import json
import discord
from discord.ext import commands

config = "tools/config.json"
with open(config) as f:
    data = json.load(f)
TOPTOKEN = data['TOPTOKEN']

tools = "tools/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = TOPTOKEN # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    '''
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print(data)
        channel = self.bot.get_channel(788229974594158592)
        emb = discord.Embed(
            title = "Vote recieved!",
            color = color
        )
        user = self.bot.get_user(int(data["user"]))
        emb.set_author(name=user, icon_url=user.avatar_url)
        time_bad = datetime.datetime.now()
        time_good = time_bad.strftime("%b %d at %I:%M %p")
        emb.set_footer(text=time_good)
        await channel.send(embed=emb)        
        if not data["isWeekend"]:
            await user.send(f"Thanks for voting for me on top.gg!")
        if data ["isWeekend"]:
            await user.send(f"Thanks for voting for me on top.gg!")
    '''

    async def on_guild_post():
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(TopGG(bot))
