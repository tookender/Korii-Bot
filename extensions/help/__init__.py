from discord.ext import commands

from .help import HelpCog


class Help(HelpCog):
    pass


async def setup(bot):
    await bot.add_cog(Help(bot))
