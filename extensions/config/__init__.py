from .levelling import LevellingConfig


class Config(LevellingConfig):
    pass


async def setup(bot):
    await bot.add_cog(Config(bot))