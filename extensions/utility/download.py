import time
import discord
from discord import app_commands
from discord.ext import commands

from bot import Korii
import aiohttp
import humanfriendly


class DownloadCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
    
    @app_commands.command()
    async def download(self, interaction: discord.Interaction, url: str):
        response = await self.bot.session.post(
            "https://cobalt.tools/api/json",
            json=dict(
                url=url,
                vCodec="h264",
                vQuality="720",
                aFormat="mp3",
                isAudiOnly=False,
                isTTFullAudio=False,
                isAUdioMuted=False,
                dubLang=False,
                disableMetadata=False,
            ),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        
        status = response.status
        json = await response.json()

        if status != 200:
            return await interaction.response.send_message(f"❌ | {json['text']}", ephemeral=True)
        
        await interaction.response.send_message("▶️ | downloading...", ephemeral=True)

        start = time.time()

        url = json["url"]
        video = await self.bot.session.get(url)
        video_data = await video.read()
        filename = aiohttp.parse_content_disposition(video.headers["Content-Disposition"])[1]["filename"]

        if video.ok is False:
            json = await video.json()
            return await interaction.response.send_message(f"❌ | {json['text']}", ephemeral=True)

        await interaction.edit_original_response(content="▶️ | uploading...")

        expiry = "1"

        form = aiohttp.FormData()
        form.add_field("file", video_data, filename=filename)
        form.add_field("expires", expiry)

        hresp = await self.bot.session.post("https://0x0.st", data=form)

        text = await hresp.text()

        end = time.time()
        took = end - start
        formatted_took = humanfriendly.format_timespan(int(took))

        await interaction.edit_original_response(content=f"✅ | process took {formatted_took}, file expires in {expiry} hour(s): {text}")