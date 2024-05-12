from .arb6mans import Arb6Mans


async def setup(bot):
    await bot.add_cog(Arb6Mans(bot))