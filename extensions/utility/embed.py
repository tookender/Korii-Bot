from discord import app_commands

from utils import Interaction
from views.embed import EmbedView

from ._base import UtilityBase


class EmbedCog(UtilityBase):
    @app_commands.command(description="Create a custom embed.")
    @app_commands.describe(ephemeral="If the message should be sent ephemerally or not.")
    async def embed(self, interaction: Interaction, ephemeral: bool = False):
        view = EmbedView(interaction.user)

        return await interaction.response.send_message(view=view, embed=view.default_embed(), ephemeral=ephemeral)
