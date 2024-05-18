from typing import Any, TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from bot import Korii
else:
    from discord.ext.commands import bot as Korii

class Cog(commands.Cog):
    __slots__ = "bot"

    def __init__(self, bot: Korii, *args: Any, **kwargs: Any) -> None:
        self.bot: Korii = bot

        super().__init__(*args, **kwargs)
