import discord, json
from discord.ext import commands, menus

class Source(menus.ListPageSource):
    '''Formatting for help command.'''
    def __init__(self, data):
        super().__init__(data, per_page=1)

class HelpCommand(commands.HelpCommand):
    '''Help Command.'''
    def __init__(self):
        super().__init__(command_attrs={
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': 'Shows help about the bot, a command, or a category',
            "aliases": ["h"]
        })

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Command List', colour=self.context.bot.color)
        description = self.context.bot.description
        if description:
            embed.description = description

        for cog, commands in mapping.items():
            name = 'No Category' if cog is None else cog.qualified_name
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                value = '\u2002'.join(c.name for c in commands)
                if cog and cog.description:
                    value = '{0}\n{1}'.format(cog.description, value)

                embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text='Use {0}{1} [command|module] for more info.'.format(self.clean_prefix, self.invoked_with))#self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        use = await command.can_run(self.context)
        embed = discord.Embed(title=command.name,
                              description=command.help or "No info available.",
                              colour=self.context.bot.color)
        embed.add_field(name="Usage:", value=f"{command.name} {command.signature}", inline=False)
        embed.add_field(name="Category:", value=f"{command.cog_name}", inline=False)
        if command.aliases:
            embed.add_field(name="Aliases:", value="\n".join(command.aliases), inline=False)
        embed.set_footer(text=self.context.bot.footer)
        return await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name,
                              description=cog.description or "No info available.",
                              colour=self.context.bot.color)
        embed.add_field(name="Commands:", value="\n".join(f"**{command}** - {command.short_doc}" for command in cog.get_commands()) or "None")
        embed.set_footer(text=self.context.bot.footer)
        return await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.name,
                              description=group.help or "No info available.",
                              colour=self.context.bot.color)
        '''
        embed.add_field(name="Usage:", value=f"{group.name} {group.signature}", inline=False)
        '''
        embed.add_field(name="Category:", value=f"{group.cog_name}", inline=False)
        if group.aliases:
            embed.add_field(name="Aliases:", value="\n".join(group.aliases), inline=False)
        embed.add_field(name="Commands:", value="\n".join(str(command) for command in group.walk_commands()) or "None")
        embed.set_footer(text=self.context.bot.footer)
        return await self.context.send(embed=embed)


def setup(bot):
    bot.help_command = HelpCommand()
