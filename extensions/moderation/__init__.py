
from .basic import BasicCog


class Moderation(BasicCog):
    pass


async def setup(bot):
    await bot.add_cog(Moderation(bot))
