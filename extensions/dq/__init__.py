from .calculators import CalculatorsCog

class DungeonQuest(CalculatorsCog):
    pass


async def setup(bot):
    await bot.add_cog(DungeonQuest(bot))
