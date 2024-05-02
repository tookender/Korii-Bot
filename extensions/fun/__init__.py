from .dog import DogCog
from .actions import ActionsCog
from .random import RandomCog


class Fun(ActionsCog, RandomCog, DogCog):
    pass


async def setup(bot):
    await bot.add_cog(Fun(bot))
