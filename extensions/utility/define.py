from discord import app_commands
from discord.ext import commands

from utils import Embed
from utils.definition import get_word_details

from ._base import UtilityBase


class DefineCog(UtilityBase):
    @commands.hybrid_command(description="Get the definition of any word.")
    @app_commands.describe(word="The word you want the definition of.")
    async def define(self, ctx, word: str):
        word_details = await get_word_details(self.bot, word)
        nl = "\n"

        embed = Embed(
            title=f"{word_details['syllable']} {word_details['pronunciation']}",
            description=f"{word_details['word_type']}\n{nl.join(word_details['definitions'][:3])}",
        )

        embed.add_field(name="Etymology", value=word_details["etymology"])

        return await ctx.send(embed=embed)
