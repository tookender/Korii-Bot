import random

import discord
from bot import Korii
from discord import app_commands
from discord.ext import commands
from bot.utilities.embed import Embed


class AnimalsCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    animals = app_commands.Group(name="animals", description="Shows cute pictures and facts about animals.")

    async def send_animal(
        self, interaction: discord.Interaction, animal: str, ephemeral: bool = False
    ):
        valid_animals = [
            "bird",
            "cat",
            "dog",
            "fox",
            "kangaroo",
            "koala",
            "panda",
            "raccoon",
            "red_panda",
        ]
        phrases = ["A very cute", "An adorable", "Very cute and adorable"]

        if animal not in valid_animals:
            raise KeyError

        request = await self.bot.session.get(
            f"https://some-random-api.ml/animal/{animal}"
        )
        json = await request.json()
        image, fact = json["image"], json["fact"]

        embed = Embed(title=f"{random.choice(phrases)} {animal}", description=fact)
        embed.set_author(name="Link", url=json["image"])
        embed.set_image(url=image)

        return await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    @animals.command(description="Sends a cute picture of a bird and a fact.")
    async def bird(self, interaction: discord.Interaction, ephemeral: bool = False):
        return await self.send_animal(interaction, "bird", ephemeral)

    @animals.command(description="Sends a cute picture of a cat and a fact.")
    async def cat(self, interaction: discord.Interaction, ephemeral: bool = False):
        return await self.send_animal(interaction, "cat", ephemeral)

    @animals.command(description="Sends a cute picture of a dog and a fact.")
    async def dog(self, interaction: discord.Interaction, ephemeral: bool = False):
        return await self.send_animal(interaction, "dog", ephemeral)

    @animals.command(description="Sends a cute picture of a fox and a fact.")
    async def fox(self, interaction: discord.Interaction, ephemeral: bool = False):
        return await self.send_animal(interaction, "fox", ephemeral)

    @animals.command(description="Sends a cute picture of a kangaroo and a fact.")
    async def kangaroo(self, interaction: discord.Interaction, ephemeral: bool = False):
        return await self.send_animal(interaction, "kangaroo", ephemeral)

    @animals.command(description="Sends a cute picture of a koala and a fact.")
    async def koala(self, interaction: discord.Interaction, ephemeral: bool = False):
        return await self.send_animal(interaction, "koala", ephemeral)

    @animals.command(description="Sends a cute picture of a panda and a fact.")
    async def panda(self, interaction: discord.Interaction, ephemeral: bool = False):
        return await self.send_animal(interaction, "panda", ephemeral)

    @animals.command(description="Sends a cute picture of a raccoon and a fact.")
    async def raccoon(self, interaction: discord.Interaction, ephemeral: bool = False):
        return await self.send_animal(interaction, "raccoon", ephemeral)

    @animals.command(description="Sends a cute picture of a red panda and a fact.")
    async def red_panda(self, interaction: discord.Interaction, ephemeral: bool = False):
        return await self.send_animal(interaction, "red_panda", ephemeral)
