import discord
from discord import app_commands
from discord.ext import commands

from utils import Interaction, Cog
from views.embed import EmbedView


class EmbedCog(Cog):
    @app_commands.command(description="Create a custom embed.")
    @app_commands.describe(ephemeral="If the message should be sent ephemerally or not.")
    async def embed(self, interaction: Interaction, ephemeral: bool = False):
        view = EmbedView(interaction.user)

        return await interaction.response.send_message(view=view, embed=view.default_embed(), ephemeral=ephemeral)
