from discord import app_commands
from discord.ext import commands

from utils import Interaction, utils

from ._base import UtilityBase


class PingCog(UtilityBase):
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
