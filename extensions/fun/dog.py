from discord import app_commands

from utils import Embed, Interaction

from ._base import FunBase


class DogCog(FunBase):
    @app_commands.command(description="Sends a random image of my dog :D")
    @app_commands.guild_only()
    @app_commands.describe(ephemeral="If the message should be private or not.")
    async def dog(self, interaction: Interaction, ephemeral: bool = False):
        request = await self.bot.session.get("https://korino.dev/api/doggo")
        if request.status != 200:
            return await interaction.response.send_message("👻 | an unknown error occurred!")

        json = await request.json()

        embed = Embed(title="Doggo :D", color=self.bot.color)

        embed.set_image(url=json["data"]["url"])
        embed.set_author(name="Visit korino.dev/doggo for more", url="https://korino.dev/doggo")

        return await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
