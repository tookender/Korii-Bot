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


import discord
from discord import app_commands
from discord.ext import commands

from utils import Interaction
from views.embed import EmbedView


class EmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(description="Create a custom embed.")
    @app_commands.describe(ephemeral="If the message should be sent ephemerally or not.")
    async def embed(self, interaction: Interaction, ephemeral: bool = False):
        view = EmbedView(interaction.user)

        return await interaction.response.send_message(view=view, embed=view.default_embed(), ephemeral=ephemeral)
