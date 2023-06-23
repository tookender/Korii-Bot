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
        starter_embed = discord.Embed(
            title="This is an example of a title",
            description=f"This is an example of the description. It can be very long and wordy.\nIt can even have new lines, adding ` \\n` will add a new line.\nIt also has __**MARKDOWN SUPPORT**__.\nUnlike the title, you can also use custom emojis in here {interaction.client.E['star']}",
            color=discord.Color.random()
        )

        return await interaction.response.send_message(view=EmbedView(interaction.user), embed=starter_embed, ephemeral=ephemeral)
