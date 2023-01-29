from typing import Optional

import discord
from bot import Korii
from discord import app_commands
from discord.ext import commands
from bot.utilities.embed import Embed


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
