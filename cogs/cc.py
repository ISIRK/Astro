from discord.ext import commands


# The check to ensure this is the guild used where the command was made
def guild_check(_custom_commands):
    async def predicate(ctx):
        return _custom_commands.get(ctx.command.qualified_name) and ctx.guild.id in _custom_commands.get(ctx.command.qualified_name)
    return commands.check(predicate)

class cc(commands.Cog):

    """ Each entry in _custom_commands will look like this:
    {
        "command_name": {
            guild_id: "This guild's output",
            guild_id2: "This other guild's output",
        }
    }
    """
    _custom_commands = {}

    @commands.is_owner()
    @commands.command()
    async def add_command(self, ctx, name, *, output):
        # First check if there's a custom command with that name already
        existing_command = self._custom_commands.get(name)
        # Check if there's a built in command, we don't want to override that
        if existing_command is None and ctx.bot.get_command(name):
            return await ctx.send(f"A built in command with the name {name} is already registered")

        # Now, if the command already exists then we just need to add/override the message for this guild
        if existing_command:
            self._custom_commands[name][ctx.guild.id] = output
        # Otherwise, we need to create the command object
        else:
            @commands.is_owner()
            @commands.command(name=name, help=f"Custom command: Outputs your custom provided output")
            @guild_check(self._custom_commands)
            async def cmd(self, ctx):
                await ctx.send(self._custom_commands[ctx.invoked_with][ctx.guild.id])

            cmd.cog = self
            # And add it to the cog and the bot
            self.__cog_commands__ = self.__cog_commands__ + (cmd,)
            ctx.bot.add_command(cmd)
            # Now add it to our list of custom commands
            self._custom_commands[name] = {ctx.guild.id: output}
        await ctx.send(f"Added a command called {name}")

    @commands.is_owner()
    @commands.command()
    async def remove_command(self, ctx, name):
        # Make sure it's actually a custom command, to avoid removing a real command
        if name not in self._custom_commands or ctx.guild.id not in self._custom_commands[name]:
            return await ctx.send(f"There is no custom command called {name}")
        # All that technically has to be removed, is our guild from the dict for the command
        del self._custom_commands[name][ctx.guild.id]
        await ctx.send(f"Removed a command called {name}")

def setup(bot):
    bot.add_cog(cc(bot))
