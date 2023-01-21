from extensions.events.guild import GuildCog


class Events(GuildCog):
    pass


async def setup(bot):
    await bot.add_cog(Events(bot))
