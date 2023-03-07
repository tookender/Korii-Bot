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

import time

import discord
from discord import app_commands
from discord.ext import commands

from bot import Embed, Korii


class PingCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    def spaces(self, ping: float) -> str:
        return " " * (9 - len(str(round(ping, 2))))

    @app_commands.command(description="Pong.")
    @app_commands.checks.cooldown(1, 5)
    async def ping(self, interaction: discord.Interaction):
        pings = []

        start_typing = time.perf_counter()
        await interaction.response.defer(thinking=True)
        end_typing = time.perf_counter()
        total_typing = (end_typing - start_typing) * 1000

        start_message = time.perf_counter()
        await interaction.followup.send("🏓 | Pong!")
        end_message = time.perf_counter()
        total_message = (end_message - start_message) * 1000

        pool_start = time.perf_counter()
        await self.bot.pool.fetch("SELECT 1")
        pool_end = time.perf_counter()
        total_pool = (pool_end - pool_start) * 1000

        total_latency = self.bot.latency * 1000

        pings.extend([total_typing, total_message, total_pool, total_latency])
        total_average = sum(pings) / len(pings)

        return await interaction.edit_original_response(
            content=f"🌐 | `Websocket  `**`{round(total_latency, 2)}ms{self.spaces(total_latency)}`**\n"
                    f"⌨️ | `Typing     `**`{round(total_typing, 2)}ms{self.spaces(total_typing)}`**\n"
                    f"💬 | `Message    `**`{round(total_message, 2)}ms{self.spaces(total_message)}`**\n" 
                    f"🐘 | `Database   `**`{round(total_pool, 2)}ms{self.spaces(total_pool)}`**\n"
                    f"⚙️ | `Average    `**`{round(total_average, 2)}ms{self.spaces(total_average)}`**"
        )

