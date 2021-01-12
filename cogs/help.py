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
        embed = discord.Embed(title=f"Help Menu for {menu.ctx.guild.me.nick}",
                              description="A bot Made by isirk",
                              color=color)
        embed.set_footer(text=f"Page {menu.current_page + 1}/{self.get_max_pages()} | {footer}")
        _commands = "\n".join(str(command) for command in page[1].get_commands()) or "No commands in this category."
        embed.add_field(name=page[0], value=_commands)
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
        pages = MenusHelp(source=Source(data), clear_reactions_after=True)
        await pages.start(self.context)
        try:
            await self.context.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        except discord.Forbidden:
            pass

    async def send_command_help(self, command):
        use = await command.can_run(self.context)
        embed = discord.Embed(title=command.name,
                              description=command.help or "No info available.",
                              colour=color)
        embed.add_field(name="Usage:", value=f"{command.name} {command.signature}", inline=False)
        embed.add_field(name="Category:", value=f"{command.cog_name}", inline=False)
        try:
            use = await command.can_run(self.context)
            if use:
                use = "Yes"
            else:
                use = "No"
        except commands.CommandError:
            use = "No"
        embed.add_field(name="Can Use:", value=use)
        if command.aliases:
            embed.add_field(name="Aliases:", value="\n".join(command.aliases), inline=False)
        embed.set_footer(text=footer)
        return await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f"Help on Category `{cog.qualified_name}`",
                              description=cog.description or "No info available.",
                              colour=color)
        embed.add_field(name="Commands in this Category:", value="\n".join(str(command) for command in cog.get_commands()) or "None")
        embed.set_footer(text=f"Use {menu.ctx.prefix}help [command|module] for more info on a command.")
        return await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"Help on Command Group `{group.name}`",
                              description=group.help or "No info available.",
                              colour=color)
        embed.add_field(name="Signature:", value=f"{group.name} {group.signature}", inline=False)
        embed.add_field(name="Category:", value=f"{group.cog_name}", inline=False)
        embed.add_field(name="Aliases:", value="\n".join(group.aliases) or "None", inline=False)
        embed.add_field(name="Commands in this Group:", value="\n".join(str(command) for command in group.walk_commands()) or "None")
        embed.set_footer(text=f"Use {menu.ctx.prefix}help [command|module] for more info on a command.")
        return await self.context.send(embed=embed)


def setup(bot):
    bot.help_command = HelpCommand()