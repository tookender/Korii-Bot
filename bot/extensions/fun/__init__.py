from .animals import AnimalsCog
from .random import RandomCog


class Fun(RandomCog, AnimalsCog):
    pass


async def setup(bot):
    await bot.add_cog(Fun(bot))
