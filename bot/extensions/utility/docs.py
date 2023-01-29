import discord
from bot import Korii
from discord import app_commands
from discord.ext import commands
from bot.utilities.embed import Embed


class EmbedCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @app_commands.command(description="A command to search sphinx documentations.")
    @app_commands.describe(location="The documentation. This can be an URL.")
    @app_commands.describe(query="What you want to search for.")
    async def rtfm(
        self,
        interaction: discord.Interaction,
        location: str,
        querty: str,
    ):
        request = await self.bot.session.get("https://idevision.net/api/public/rtfm.sphinx", params={"query": query, "location": location})

        await interaction.response.send_message(embed=embed)
