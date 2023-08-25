from typing import Any, Optional

import discord


class Embed(discord.Embed):
    def __init__(self, executed: Optional[str] = None, requested: Optional[str] = None, colour=0x10B981, **kwargs):
        super().__init__(colour=colour, **kwargs)

        if executed:
            self.set_footer(text=f"Executed by {executed}")

        if requested:
            self.set_footer(text=f"Requested by {requested}")

    def add_field(self, *, name: Any, value: Any, inline: bool = True, title: bool = True):
        super().add_field(name=name.title() if title else name, value=value, inline=inline)
