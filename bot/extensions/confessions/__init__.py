from extensions.confessions.commands import CommandsCog


class Confessions(CommandsCog):
    pass


async def setup(bot):
    await bot.add_cog(Confessions(bot))
