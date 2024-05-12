from discord.ext import commands


def setup(bot):
    bot.add_cog(Admin(bot))


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def load(self, ctx, module):
        """Loads a module."""

        # You will need to set your own ID here
        if ctx.author.id != 256963559395819520:
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            self.bot.load_extension(f'cogs.{module}')
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    async def unload(self, ctx, module):
        """Unloads a module."""
        # You will need to set your own ID here
        if ctx.author.id != 256963559395819520:
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            self.bot.unload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, module):
        """Reloads a module."""
        # You will need to set your own ID here
        if ctx.author.id != 256963559395819520:
            await ctx.send("You do not have permission to use this command.")
            return
        try:
            self.bot.unload_extension(f'cogs.{module}')
            self.bot.load_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')
