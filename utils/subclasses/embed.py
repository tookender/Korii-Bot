"""
Korii Bot: A multi-purpose bot with swag 😎
Copyright (C) 2023 Ender2K89

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Any, Optional

import discord


class Embed(discord.Embed):
    def __init__(
        self,
        executed: Optional[str] = None,
        requested: Optional[str] = None,
        colour=0x10B981,
        **kwargs,
    ) -> None:
        super().__init__(colour=colour, **kwargs)

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
        super().add_field(name=name.title() if title else name, value=value, inline=inline)
