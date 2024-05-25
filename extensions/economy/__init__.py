from .bank import BankCog
from .basic import BasicCog
from .gambling import GamblingCog
from .work import WorkCog


class Economy(BasicCog, GamblingCog, WorkCog, BankCog):
    pass


async def setup(bot):
    await bot.add_cog(Economy(bot))
