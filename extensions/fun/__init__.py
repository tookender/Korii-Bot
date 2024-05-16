from .actions import ActionsCog
from .dog import DogCog
from .random import RandomCog


class Fun(DogCog, ActionsCog, RandomCog):
    pass


async def setup(bot):
    await bot.add_cog(Fun(bot))
