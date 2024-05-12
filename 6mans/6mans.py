from redbot.core import commands

class lilArb6Mans(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def arb6mans(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")