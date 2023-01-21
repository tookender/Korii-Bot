from typing import Any, Optional

import discord


class Embed(discord.Embed):
    def __init__(
        self,
        executed: Optional[str] = None,
        requested: Optional[str] = None,
        **kwargs,
    ):
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
        no_title: bool = False,
    ):
        super().add_field(
            name=name.title() if no_title else name,
            value=value,
            inline=inline,
        )
