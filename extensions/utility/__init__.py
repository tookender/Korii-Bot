from .config import ConfigCog
from .info import InfoCog
from .neofetch import NeofetchCog
from .ping import PingCog
from .source import SourceCog
from .embed import EmbedCog
from .translate import TranslateCog
from .spotify import SpotifyCog


class Utility(ConfigCog, InfoCog, NeofetchCog, PingCog, SourceCog, EmbedCog, TranslateCog, SpotifyCog):
    pass


async def setup(bot):
    await bot.add_cog(Utility(bot))
