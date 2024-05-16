import subprocess

from discord import app_commands
from discord.ext import commands

from utils import Interaction

from ._base import UtilityBase


class NeofetchCog(UtilityBase):
    @app_commands.command(description="Neofetch but in Discord.")
    @app_commands.checks.cooldown(1, 5)
    async def neofetch(self, interaction: Interaction):
        output = subprocess.check_output(["neofetch", "--off"], shell=True)

        return await interaction.response.send_message(
            "```ansi\n" f"{output.decode()[:-311][11:]}\n" "```",
        )
