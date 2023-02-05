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
