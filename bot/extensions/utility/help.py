import random

import discord
from bot import Korii
from discord import app_commands
from discord.ext import commands
from utilities.classes.embed import Embed


class HelpCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    @app_commands.command(description="View help on the bot.")
    async def help(self, interaction: discord.Interaction):
        bar = [
            f"{self.bot.E['github']} [`Source`]({self.bot.source})",
            f"{self.bot.E['invite']} [`Invite`]({self.bot.invite})",
            f"{self.bot.E['globe']} [`Website`]({self.bot.website})",
            f"{self.bot.E['book']} [`Docs`]({self.bot.docs})",
        ]

        embed = Embed(
            title="Welcome to Korii ✨",
            description=" **|** ".join(bar),
            color=discord.Colour.from_hsv(random.random(), 0.28, 0.97),
        )

        return await interaction.response.send_message(embed=embed)
