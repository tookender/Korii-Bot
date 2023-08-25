from .actions import ActionsCog
from .animals import AnimalsCog
from .random import RandomCog


class Fun(ActionsCog, RandomCog, AnimalsCog):
    pass


async def setup(bot):
    await bot.add_cog(Fun(bot))
