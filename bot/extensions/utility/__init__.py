from extensions.utility.help import HelpCog
from extensions.utility.info import InfoCog


class Utility(InfoCog, HelpCog):
    pass


async def setup(bot):
    await bot.add_cog(Utility(bot))
