
from .faq import FAQCog, FAQView
from .introductions import IntroductionsCog, IntroductionsView
from .welcome import WelcomeCog, WelcomeView


class World(FAQCog, IntroductionsCog, WelcomeCog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(FAQView())
        self.bot.add_view(IntroductionsView())
        self.bot.add_view(WelcomeView())
    pass


async def setup(bot):
    await bot.add_cog(World(bot))
