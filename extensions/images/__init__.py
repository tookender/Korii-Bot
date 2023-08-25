
from .jeyy_api import JeyyAPICog


class Images(JeyyAPICog):
    pass


async def setup(bot):
    await bot.add_cog(Images(bot))
