import discord, json
from discord.ext import commands, menus

class HelpCommand(commands.HelpCommand):
    '''Help Command.'''
    def __init__(self):
        super().__init__(command_attrs={
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': 'Shows help about the bot, a command, or a category',
            "aliases": ["h"]
        })

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Command List', description=self.context.bot.description, url="https://asksirk.com/bot/commands", colour=self.context.bot.color)

        name = 'No Category' if cmd.cog.qualified_name is None else cmd.cog.qualified_name
        filtered = await self.filter_commands(self.contect.bot.commands, sort=True)
        if filtered:
            value = ' '.join(f'`{c.name}`' for c in self.context.bot.commands)
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text='Use {0}{1} [command|module] for more info.'.format(self.clean_prefix, self.invoked_with))#self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=command.name,
                              description=command.help or "No info available.",
                              colour=self.context.bot.color)
        embed.add_field(name="Usage:", value=f"{command.name} {command.signature}", inline=False)
        embed.add_field(name="Category:", value=f"{command.cog_name}", inline=False)
        try:
            can_run = await command.can_run(self.context)
            if can_run:
                can_run = "<:green_tick:802239639712563241>"
            else:
                can_run = "<:red_tick:802239639561437204>"
        except commands.CommandError:
            can_run = "<:red_tick:802239639561437204>"
        embed.add_field(name="Can use:", value=can_run)
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
