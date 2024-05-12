import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(ChatCommands(bot))


class ChatCommands(commands.Cog, name="Chat Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, name="clearChat")
    @commands.has_permissions(manage_channels=True)
    async def clear_chat(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
