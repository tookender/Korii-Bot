
import io
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.app_commands import Choice

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
    async def images(self, interaction: Interaction, type: ..., user: Optional[discord.Member] = None):
        assert isinstance(interaction.user, discord.Member)

        if not user:
            user = interaction.user
        
        ...