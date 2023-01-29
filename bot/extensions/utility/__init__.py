from .help import HelpCog
from .info import InfoCog


class Utility(InfoCog, HelpCog):
    pass


async def setup(bot):
    await bot.add_cog(Utility(bot))
