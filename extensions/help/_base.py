from discord.ext import commands

from bot import Korii
from utils.context import CustomContext


class HelpBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.bot.remove_command("help")

    async def get_prefix(self, ctx: CustomContext) -> str:
        if isinstance(ctx, commands.Context):
            prefix = "s!"
        else:
            prefix = "/"

        return prefix
