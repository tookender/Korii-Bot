from typing import Any, Optional

from discord.ext import commands

from bot import Korii


class Cog(commands.Cog):
    __slots__ = "bot"

    def __init__(self, bot: Korii, *args: Any, **kwargs: Any) -> None:
        self.bot: Korii = bot

        super().__init__(*args, **kwargs)
