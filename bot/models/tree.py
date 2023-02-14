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

from typing import TYPE_CHECKING

import discord
from discord import Embed, app_commands

if TYPE_CHECKING:
    from bot import Korii
else:
    from discord.ext.commands import AutoShardedBot as Korii


class CommandTree(app_commands.CommandTree):
    client: Korii

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if interaction.command:
            embed = Embed(
                title=f"{self.client.E['close']} Error",
                color=discord.Color.red(),
            )

            embed.add_field(name="Reason", value=error)

        embed = Embed(
            title=f"{self.client.E['close']} Unexpected Error",
            description="We are sorry for this inconvenience.\n"
            "The developers have been notified about this and will fix it.",
            color=discord.Color.red(),
        )

        embed.add_field(name="Reason", value=error)

        if interaction.response.is_done():
            return await interaction.followup.send(embed=embed, ephemeral=True)

        return await interaction.response.send_message(embed=embed, ephemeral=True)
