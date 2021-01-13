import discord, json
from discord.ext import commands, menus

tools = "tools/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class Source(menus.ListPageSource):
    '''Formatting for help command.'''
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu: menus.MenuPages, page):
        embed = discord.Embed(color=color)
        '''
        title=f"Help Menu for {menu.ctx.guild.me.display_name}",
                              description=menu.ctx.bot.description,
                              
        '''
        embed.set_footer(text=f"Page {menu.current_page + 1}/{self.get_max_pages()} | {footer}")
        if menu.current_page == 0:
            embed.add_field(name=f"{ctx.guild.me.display_name}", value=menu.ctx.bot.description)
        else:
            _commands = "\n".join(str(command) for command in page[1].get_commands()) or "No commands in this category."
            #embed.add_field(name=page[0], value=_commands)
            embed.title = page[0]
            embed.description = _commands
        return embed


class MenusHelp(menus.MenuPages):
    '''Help command utilizing menus.'''


class HelpCommand(commands.HelpCommand):
    '''Help Command.'''
    def __init__(self):
        super().__init__(command_attrs={
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': 'Shows help about the bot, a command, or a category',
            "aliases": ["h"]
        })

    async def send_bot_help(self, _):
        data = {0: None}
        data.update({num: cog_pair for num, cog_pair in enumerate(self.context.bot.cogs.items(), start=0)})
        pages = MenusHelp(source=Source(data), delete_message_after=True) #clear_reactions_after=True)
        await pages.start(self.context)

    async def send_command_help(self, command):
        use = await command.can_run(self.context)
        embed = discord.Embed(title=command.name,
                              description=command.help or "No info available.",
                              colour=color)
        embed.add_field(name="Usage:", value=f"{command.name} {command.signature}", inline=False)
        embed.add_field(name="Category:", value=f"{command.cog_name}", inline=False)
        if command.aliases:
            embed.add_field(name="Aliases:", value="\n".join(command.aliases), inline=False)
        embed.set_footer(text=footer)
        return await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name,
                              description=cog.description or "No info available.",
                              colour=color)
        embed.add_field(name="Commands:", value="\n".join(str(command) for command in cog.get_commands()) or "None")
        embed.set_footer(text=footer)
        return await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.name,
                              description=group.help or "No info available.",
                              colour=color)
        '''
        embed.add_field(name="Usage:", value=f"{group.name} {group.signature}", inline=False)
        '''
        embed.add_field(name="Category:", value=f"{group.cog_name}", inline=False)
        if group.aliases:
            embed.add_field(name="Aliases:", value="\n".join(gruop.aliases), inline=False)
        embed.add_field(name="Commands:", value="\n".join(str(command) for command in group.walk_commands()) or "None")
        embed.set_footer(text=footer)
        return await self.context.send(embed=embed)


def setup(bot):
    bot.help_command = HelpCommand()
