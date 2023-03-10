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

import random

from bot import Korii, Embed, Interaction
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice


class AnimalsCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    @app_commands.command(description="Shows cute pictures and facts about animals.")
    @app_commands.describe(animal="The animal you'd like to see.")
    @app_commands.describe(ephemeral="If the message should be private or not.")
    @app_commands.choices(
        animal=[
            Choice(name="🐦 Bird", value="bird"),
            Choice(name="😸 Cat", value="cat"),
            Choice(name="🐶 Dog", value="dog"),
            Choice(name="🦊 Fox", value="fox"),
            Choice(name="🦘 Kangaroo", value="kangaroo"),
            Choice(name="🐨 Koala", value="koala"),
            Choice(name="🐼 Panda", value="panda"),
            Choice(name="🦝 Raccoon", value="raccoon"),
            Choice(name="🐼 Red Panda", value="red_panda")
        ]
    )
    async def animal(self, interaction: Interaction, animal: Choice[str], ephemeral: bool = False):
        phrases = ["A very cute", "An adorable", "Very cute and adorable"]

        request = await self.bot.session.get(
            f"https://some-random-api.ml/animal/{animal.value}"
        )
        json = await request.json()
        image, fact = json["image"], json["fact"]

        embed = Embed(title=f"{random.choice(phrases)} {animal.value}", description=fact)
        embed.set_image(url=image)

        return await interaction.response.send_message(embed=embed, ephemeral=ephemeral)