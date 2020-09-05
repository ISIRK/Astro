import discord
from discord import Embed
client = discord.Client()



@client.event
async def on_ready():
    print('{0.user} is up and running'.format(client))
    await client.change_presence(activity=discord.Game(name="a game"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('^help'):

        helpembed = discord.Embed(title="Help", description="**Astro Bot** \n A Utilities Discord Bot with reliability and simplicity\n Made By isirk#0001", color=0x7289DA)
        helpembed.add_field(name= ":gear: Updates", value="Version 0.2 \n :inbox_tray: Finished help command \n :outbox_tray: Making Kick Command", inline=True)
        helpembed.add_field(name= ":link: Links", value="[Bot Site](https://asksirk.com/Astro) \n [Github Repository](https://github.com/ISIRK/Astro) \n [Patreon](https://www.patreon.com/Astro_Bot)")
        helpembed.set_footer(text="Astro Bot | discord.gg/7yZqHfG")

        await message.channel.send(embed=helpembed)

client.run('NzUxNDQ3OTk1MjcwMTY4NTg2.X1JOew.AU7LaGLfrdE6eNoZOCapbnAG-Gg')