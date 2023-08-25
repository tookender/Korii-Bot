
from discord.ext import commands

from .commands import CommandsCog
from .events import EventsCog


class Levelling(EventsCog, CommandsCog): # EventsCog needs to be first, it adds attributes
    pass


async def setup(bot):
    await bot.add_cog(Levelling(bot))
