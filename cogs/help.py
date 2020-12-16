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
import asyncio, json

import discord
from discord.ext import commands, menus

tools = "tools/tools.json"
with open(tools) as f:
    data = json.load(f)
footer = data['FOOTER']
color = int(data['COLOR'], 16)

class EmbedMenu(menus.Menu):
    def __init__(self, pages):
        super().__init__(delete_message_after=True)
        self.pages = pages
        self.current_page = 0

    def _skip_when(self):
        return len(self.pages) <= 2

    async def update_page(self):
        embed = self.pages[self.current_page]
        await self.message.edit(embed=embed)

    @menus.button("\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f", skip_if=_skip_when)
    async def jump_to_first(self, payload):
        self.current_page = 0
        await self.update_page()

    @menus.button("\N{BLACK LEFT-POINTING TRIANGLE}\ufe0f")
    async def previous_page(self, payload):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_page()

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def stop_pages(self, payload):
        self.stop()

    @menus.button("\N{BLACK RIGHT-POINTING TRIANGLE}\ufe0f")
    async def next_page(self, payload):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.update_page()

    @menus.button("\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f", skip_if=_skip_when)
    async def jump_to_last(self, payload):
        self.current_page = len(self.pages) - 1
        await self.update_page()

    @menus.button("\N{INPUT SYMBOL FOR NUMBERS}")
    async def jump_to(self, payload):
        m = await self.message.channel.send("Which page would you like to go to?")
        try:
            n = await self.bot.wait_for("message", check=lambda m: m.author == self.ctx.author and m.channel == self.ctx.channel and m.content.isdigit(), timeout=30)
        except asyncio.TimeoutError:
            return
        except:
            raise
        else:
            self.current_page = int(n.content) - 1
            await self.update_page()
        finally:
            await m.delete()
            try:
                await n.delete()
            except:
                pass

    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=self.pages[self.current_page])


class PaginatedHelpCommand(commands.HelpCommand):
    def recursive_command_format(self, command, *, indent=1, subc=0):
        yield ('' if indent == 1 else '├' if subc != 0 else '└') + f'**{command.qualified_name}** - {command.short_doc}'
        if isinstance(command, commands.Group):
            last = len(command.commands) - 1
            for i, command in enumerate(command.commands):
                yield from self.recursive_command_format(command, indent=indent+1, subc=last)
                last -= 1

    def format_commands(self, cog, cmds, *, pages):
        if not cmds:
            return

        pg = commands.Paginator(max_size=2000, prefix='', suffix='')

        for command in cmds:
            for line in self.recursive_command_format(command):
                pg.add_line(line)

        for desc in pg.pages:
            embed = discord.Embed(colour=color) #, title=cog.qualified_name if cog else 'Unsorted'
            name = cog.qualified_name if cog else 'Unsorted'
            embed.description = f'**{cog.description}**\n{desc}' if cog else f'No description\n{desc}' # {cog.description}\n #No description\n
            embed.set_footer(
                text=f'Use "{self.clean_prefix}help <command|module>" for more information.')
            pages.append(embed)

    async def send_bot_help(self, mapping):
        pages = []
        ctx = self.context

        for cog, cmds in mapping.items():
            cmds = await self.filter_commands(cmds, sort=True)
            self.format_commands(cog, cmds, pages=pages)

        total = len(pages)
        for i, embed in enumerate(pages, start=1):
            embed.title = f'Page {i}/{total}' # | {embed.title}}

        pg = EmbedMenu(pages)
        await pg.start(self.context)
        
    async def send_cog_help(self, cog):
        pages = []
        ctx = self.context
        self.format_commands(cog, await self.filter_commands(cog.get_commands(), sort=True), pages=pages)
        total = len(pages)
        for i, embed in enumerate(pages, start=1):
            embed.title = f'Page {i}/{total}' # : {embed.title}
        pg = EmbedMenu(pages)
        await pg.start(self.context)

    async def send_group_help(self, group):
        if not group.commands:
            return await self.send_command_help(group)
        embed = discord.Embed(colour=color)
        embed.title = f'{self.clean_prefix}{group.qualified_name} {group.signature}'
        embed.description = group.help or 'No help provided'
        embed.set_footer(
            text=f'Use "{self.clean_prefix}help <command>" for more information.')
        embed.add_field(name='Subcommands', value='\n'.join(
            f'**{c.qualified_name}** - {c.short_doc}' for c in group.commands))
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(colour=color)
        embed.title = f'{self.clean_prefix}{command.qualified_name} {command.signature}'
        embed.description = command.help or 'No help provided'
        embed.set_footer(
            text=f'Use "{self.clean_prefix}help <command>" for more information.')
        await self.context.send(embed=embed)


def setup(bot):
    bot._original_help_command = bot.help_command
    bot.help_command = PaginatedHelpCommand()


def teardown(bot):
    bot.help_command = bot._original_help_command
