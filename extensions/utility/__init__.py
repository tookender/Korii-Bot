from .config import ConfigCog
from .info import InfoCog
from .neofetch import NeofetchCog
from .ping import PingCog
from .source import SourceCog
from .embed import EmbedCog


class Utility(ConfigCog, InfoCog, NeofetchCog, PingCog, SourceCog, EmbedCog):
    pass


async def setup(bot):
    await bot.add_cog(Utility(bot))
