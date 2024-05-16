import discord
from discord import app_commands

from bot import Korii
from utils import Interaction

from ._base import UtilityBase


class TranslateCog(UtilityBase):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Translate to English",
            callback=self.translate_english,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def translate_text(self, text: str):
        query = {"dj": "1", "dt": ["sp", "t", "ld", "bd"], "client": "dict-chrome-ex", "sl": "auto", "tl": "en", "q": text}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

        try:
            response = await self.bot.session.get("https://clients5.google.com/translate_a/single", params=query, headers=headers)
            data = await response.json()
            sentences = data.get("sentences", [])

            return "".join(sentence.get("trans", "") for sentence in sentences)
        except Exception:
            return "Some error happened :("

    async def translate_english(self, interaction: Interaction, message: discord.Message) -> None:
        result = await self.translate_text(message.content)
        return await interaction.response.send_message(f"**translation result** {result}")
