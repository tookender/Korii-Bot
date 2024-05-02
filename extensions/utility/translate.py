import discord
from discord import app_commands

from utils import Interaction, Cog


class TranslateCog(Cog):
    async def translate_text(self, text: str):
        query = {"dj": "1", "dt": ["sp", "t", "ld", "bd"], "client": "dict-chrome-ex", "sl": "auto", "tl": "en", "q": text}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

        try:
            response = await self.bot.session.get("https://clients5.google.com/translate_a/single", params=query, headers=headers)
            data = await response.json()
            sentences = data["sentences"][0]["trans"]

            return sentences
        except Exception:
            return "Some error happened :("

    @app_commands.command(description="Translate the replied to message.")
    @app_commands.describe(ephemeral="If the message should be private or not.")
    @app_commands.checks.cooldown(1, 5)
    async def translate(self, interaction: Interaction, ephemeral: bool = False):
        if not interaction.message or not interaction.message.reference or not isinstance(interaction.message.reference.resolved, discord.Message):
            return await interaction.response.send_message("❌ | please reply to a message to use this command.")

        result = await self.translate_text(interaction.message.reference.resolved.content)
        return await interaction.response.send_message(f"**translation result** {result}")
