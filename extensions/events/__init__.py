from .guild import GuildCog
from .ping import PingCog
from .avatars import AvatarsCog
from .errors import ErrorsCog


class Events(AvatarsCog, PingCog, GuildCog, ErrorsCog): # PingCog needs to be first, it adds attributes
    pass


async def setup(bot):
    await bot.add_cog(Events(bot))
 