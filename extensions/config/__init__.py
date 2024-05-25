from .levelling import LevellingConfig
from .logging import LoggingConfig


class Config(LevellingConfig, LoggingConfig):
    pass


async def setup(bot):
    await bot.add_cog(Config(bot))
