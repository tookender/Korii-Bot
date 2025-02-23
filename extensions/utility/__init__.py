from .define import DefineCog
from .embed import EmbedCog
from .info import InfoCog
from .neofetch import NeofetchCog
from .ping import PingCog
from .source import SourceCog
from .spotify import SpotifyCog
from .translate import TranslateCog


class Utility(InfoCog, NeofetchCog, PingCog, SourceCog, EmbedCog, TranslateCog, SpotifyCog, DefineCog):
    pass


async def setup(bot):
    await bot.add_cog(Utility(bot))
