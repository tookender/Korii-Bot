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

import io
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from bot import Interaction, Korii


class JeyyAPICog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    images = app_commands.Group(name="images", description="Commands to manipulate images and more.")

    async def send_embed(
        self,
        interaction: Interaction,
        endpoint: str,
        url: str,
        ephemeral: bool = False,
    ):
        await interaction.response.defer(ephemeral=ephemeral)

        request = await self.bot.session.get(f"https://api.jeyy.xyz/image/{endpoint}", params={"image_url": url})
        buffer = io.BytesIO(await request.read())
        file = discord.File(buffer, filename=f"{endpoint}.gif")

        return await interaction.followup.send(file=file, ephemeral=ephemeral)

    @images.command(description="Turn the specified user's profile picture into a pyramid.")
    @app_commands.describe(user="The user's profile picture you want to turn into a pyramid.")
    @app_commands.guild_only()
    async def pyramid(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="pyramid",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Glitch the specified user's profile picture.")
    @app_commands.describe(user="The user you want to glitch the profile picture of.")
    @app_commands.guild_only()
    async def glitch(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="glitch",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Put an earthquake over the specified user's profile picture.")
    @app_commands.describe(user="The user's profile picture you want to add an earthquake effect on.")
    @app_commands.guild_only()
    async def earthquake(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="earthquake",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Pats the specified user's profile picture.")
    @app_commands.describe(user="The user's profile picture you want to pat.")
    @app_commands.guild_only()
    async def patpat(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="patpat",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Burn the specified user's profile picture.")
    @app_commands.describe(user="The user's profile picture you want to burn.")
    @app_commands.guild_only()
    async def burn(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="burn",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Explode the specified user's profile picture.")
    @app_commands.describe(user="The user's profile picture you want to explode.")
    @app_commands.guild_only()
    async def bomb(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="bomb",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Add an explicit caption over the specified user's profile picture.")
    @app_commands.describe(user="The user's profile picture you want to add an explicit caption over.")
    @app_commands.guild_only()
    async def explicit(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="explicit",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Bonk the specified user's profile picture.")
    @app_commands.describe(user="The user's profile picture you want to bonk.")
    @app_commands.guild_only()
    async def bonk(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="bonks",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Rain over the specified user's profile picture.")
    @app_commands.describe(user="The user's profile picture you want to rain over.")
    @app_commands.guild_only()
    async def rain(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="rain",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Shoot the specified user's profile picture.")
    @app_commands.describe(user="The user's profile picture you want to shoot.")
    @app_commands.guild_only()
    async def shoot(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="shoot",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Print the specified user's profile picture.")
    @app_commands.describe(user="The user's profile picture you want to print.")
    @app_commands.guild_only()
    async def print(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="print",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Turn the specified user's profile picture into a matrix.")
    @app_commands.describe(user="The user's profile picture you want to turn into a matrix.")
    @app_commands.guild_only()
    async def matrix(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="matrix",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Watch the user's profile picture on TV.")
    @app_commands.describe(user="The user's profile picture you want to watch on TV.")
    @app_commands.guild_only()
    async def tv(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="tv",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Put the specified user's profile picture in a laundry machine.")
    @app_commands.describe(user="The user's profile picture you want to put in a laundry machine.")
    @app_commands.guild_only()
    async def laundry(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="laundry",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Turn the specified user's profile picture into a pizza.")
    @app_commands.describe(user="The user's profile picture you want to turn into a pizza.")
    @app_commands.guild_only()
    async def pizza(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="pizza",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Shred the specified user's profile picture")
    @app_commands.describe(user="The user's profile picture you want to shred.")
    @app_commands.guild_only()
    async def shred(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="shred",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Turn the specified user's profile picture into balls.")
    @app_commands.describe(user="The user's profile picture you want to turn into balls.")
    @app_commands.guild_only()
    async def balls(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="balls",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Make the specified user's profile picture do complex equations.")
    @app_commands.describe(user="The user's profile picture you want to do complex equations.")
    @app_commands.guild_only()
    async def equations(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="equations",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )

    @images.command(description="Turn the specified user's profile picture into a cow.")
    @app_commands.describe(user="The user's profile picture you want to turn into a cow.")
    @app_commands.guild_only()
    async def cow(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
        ephemeral: bool = False,
    ):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user

        return await self.send_embed(
            interaction=interaction,
            endpoint="cow",
            url=user.display_avatar.url,
            ephemeral=ephemeral,
        )
