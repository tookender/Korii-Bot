from typing import Any, Optional

import discord


class Embed(discord.Embed):
    def __init__(
        self,
        executed: Optional[str] = None,
        requested: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        if not kwargs.get("color"):
            self.color = 0x2F3136

        if executed:
            self.set_footer(text=f"Executed by {executed}")

        if requested:
            self.set_footer(text=f"Requested by {requested}")

    def add_field(
        self,
        *,
        name: Any,
        value: Any,
        inline: bool = True,
        title: bool = True,
    ) -> None:
        super().add_field(
            name=name.title() if title else name, value=value, inline=inline
        )
