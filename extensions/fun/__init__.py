from .dog import DogCog
from .actions import ActionsCog
from .random import RandomCog


class Fun(DogCog, ActionsCog, RandomCog):
    pass


async def setup(bot):
    await bot.add_cog(Fun(bot))
