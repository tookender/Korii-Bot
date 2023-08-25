
import io
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

import config
from utils import Interaction, Korii

endpoints = []


class JeyyAPICog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot
        self.update_endpoints.start()

    @tasks.loop(minutes=10)
    async def update_endpoints(self):
        await self.bot.wait_until_ready()
        
        headers = {"Authorization": f"Bearer {config.JEYY_API_TOKEN}"}
        request = await self.bot.session.get("https://api.jeyy.xyz/v2/general/endpoints", headers=headers)

        json = await request.json()

        for item in json:
            if "image" in item:
                endpoints.append("")

    async def send_embed(self, interaction: Interaction, endpoint: str, url: str, ephemeral: bool = False):
        await interaction.response.defer(ephemeral=ephemeral)

        request = await self.bot.session.get(f"https://api.jeyy.xyz/v2/image/{endpoint}", params={"image_url": url})
        buffer = io.BytesIO(await request.read())
        file = discord.File(buffer, filename=f"{endpoint}.gif")

        return await interaction.followup.send(file=file, ephemeral=ephemeral)

    @app_commands.command(description="Imagine manipulation commands.")
    @app_commands.choices(fruits=[
        Choice(name='apple', value=1),
        Choice(name='banana', value=2),
        Choice(name='cherry', value=3),
    ])
    async def image(self, interaction: Interaction, type: endpoints, user: Optional[discord.Member] = None):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user
        
        ...
        
        

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
