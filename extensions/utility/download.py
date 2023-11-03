import time
import discord
from discord import app_commands
from discord.ext import commands

from utils import Cog
import humanfriendly


class DownloadCog(Cog):
    @app_commands.command()
    async def tiktok(self, interaction: discord.Interaction, *, url):
        await interaction.response.send_message("▶️ | downloading...")
        start = time.time()

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = await self.bot.session.post(
            "https://co.wuk.sh/api/json", json=dict(
                url=url,
                vQuality="max",
                aFormat="mp3",
                isNoTTWatermark=True,
                disableMetadata=True,
            ), headers=headers,
        )

        status = response.status
        data = await response.json()

        if status != 200:
            return await interaction.edit_original_response(content=f"❌ | {data['text']}")

        end = time.time()
        time_took = humanfriendly.format_timespan(int(end - start))

        return await interaction.edit_original_response(content=f"✅ | finished downloading in {time_took}")