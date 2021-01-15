import discord, os, json
from tools.bot import Sirk

tokenFile = "tools/config.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data['TOKEN']

bot = Sirk()

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

# also
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.load_extension("jishaku")

bot.run(token)