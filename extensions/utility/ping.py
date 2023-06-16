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

import asyncio
import time
from typing import Coroutine

from discord import app_commands
from discord.ext import commands

from bot import Korii
from utils import Interaction, utils


class PingCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    def spaces(self, ping: float) -> str:
        return " " * (9 - len(str(round(ping, 2))))

    @app_commands.command(description="Pong.")
    @app_commands.checks.cooldown(1, 5)
    async def ping(self, interaction: Interaction):
        pings = []

        typing = await utils.timeit(interaction.response.defer(thinking=True))
        message = await utils.timeit(interaction.followup.send("🏓 | Pong!"))
        pool = await utils.timeit(self.bot.pool.fetch("SELECT 1"))
        latency = self.bot.latency * 1000

        pings.extend([typing, message, pool, latency])
        total_average = sum(pings) / len(pings)

        return await interaction.edit_original_response(
            content=f"🌐 | `Websocket  `**`{round(latency, 2)}ms{self.spaces(latency)}`**\n"
            f"⌨️ | `Typing     `**`{round(typing, 2)}ms{self.spaces(typing)}`**\n"
            f"💬 | `Message    `**`{round(message, 2)}ms{self.spaces(message)}`**\n"
            f"🐘 | `Database   `**`{round(pool, 2)}ms{self.spaces(pool)}`**\n"
            f"⚙️ | `Average    `**`{round(total_average, 2)}ms{self.spaces(total_average)}`**"
        )
