from .bank import BankCog
from .basic import BasicCog
from .gambling import GamblingCog
from .work import WorkCog
from .job import JobCog
from .rewards import RewardsCog


class Economy(BasicCog, GamblingCog, WorkCog, BankCog, JobCog, RewardsCog):
    pass


async def setup(bot):
    await bot.add_cog(Economy(bot))
