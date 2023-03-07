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

import subprocess

import discord
from discord import app_commands
from discord.ext import commands

from bot import Embed, Korii


class NeofetchCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    @app_commands.command(description="Neofetch but in Discord.")
    @app_commands.checks.cooldown(1, 5)
    async def neofetch(self, interaction: discord.Interaction):
        output = subprocess.check_output(["neofetch", "--off"])

        return await interaction.response.send_message(
            "```ansi\n"
            f"{output.decode()[:-311][11:]}\n"
            "```",
        )
