from .errors import ErrorsCog
from .ghost import GhostCog
from .guild import GuildCog
from .ping import PingCog


class Events(PingCog, GuildCog, ErrorsCog, GhostCog):  # PingCog needs to be first, it adds attributes
    pass


async def setup(bot):
    await bot.add_cog(Events(bot))
