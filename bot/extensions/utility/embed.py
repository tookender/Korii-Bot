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

from typing import Optional

import discord
from bot import Korii
from discord import app_commands
from discord.ext import commands
from bot import Embed


class EmbedCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @app_commands.command(description="A command to create custom embeds.")
    @app_commands.describe(title="The title of the embed.")
    @app_commands.describe(description="The description of the embed.")
    @app_commands.describe(color="The color of the embed.")
    async def embed(
        self,
        interaction: discord.Interaction,
        title: str,
        description: Optional[str] = None,
        color: Optional[str] = None,
    ):
        embed = Embed(
            title=title,
            description=description,
            color=color,
        )

        await interaction.response.send_message(embed=embed)
