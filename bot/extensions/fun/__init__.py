from extensions.fun.animals import AnimalsCog
from extensions.fun.random import RandomCog


class Fun(RandomCog, AnimalsCog):
    pass


async def setup(bot):
    await bot.add_cog(Fun(bot))
