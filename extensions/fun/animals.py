import io

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from utils import Embed, Interaction, Korii


class AnimalsCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    @app_commands.command(description="Shows cute pictures and facts about animals.")
    @app_commands.describe(animal="The animal you'd like to see.")
    @app_commands.describe(ephemeral="If the message should be private or not.")
    @app_commands.guild_only()
    @app_commands.choices(
        animal=[
            Choice(name="🐶 Dog", value="https://random.dog/woof"),
            Choice(name="😺 Cat", value="https://api.thecatapi.com/v1/images/search"),
            Choice(name="🦆 Duck", value="https://random-d.uk/api/random?format=json"),
            # Choice(name="❓ Random", value="r/aww"),
        ]
    )
    async def animal(self, interaction: Interaction,
                    # animal: Optional[Choice[str]],
                    animal: Choice[str],
                    ephemeral: bool = False):
        assert interaction.guild
        # animal = animal or Choice(name="❓ Random", value="r/aww")

        request = await self.bot.session.get(animal.value)
        if request.status != 200:
            return await interaction.response.send_message("No animal found :(")
        
        name = animal.name.replace(" ", " Random ")

        if "dog" not in animal.value:
            json = await request.json()
            embed = Embed(title=name)
            embed.set_image(url=json[0]["url"])

            return await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

        filename = await request.text()
        url = f"https://random.dog/{filename}"
        filesize = interaction.guild.filesize_limit

        if filename.endswith((".mp4", ".webm")):
            request = await self.bot.session.get(url)
            if request.status != 200:
                return await interaction.response.send_message("Failed to download dog video :(")
            
            read = await request.read()
            buffer = io.BytesIO(read)

            embed = Embed(title=name)
            embed.set_image(url=f"attachments://{filename}")

            return await interaction.response.send_message(embed=embed, file=discord.File(buffer, filename=filename))
        
        embed = Embed(title=name)
        embed.set_image(url=url)
        
        return await interaction.response.send_message(embed=embed)