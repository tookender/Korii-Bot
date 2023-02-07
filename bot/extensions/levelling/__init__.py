from .events import EventsCog


class Levelling(EventsCog):
    pass


async def setup(bot):
    await bot.add_cog(Levelling(bot))
