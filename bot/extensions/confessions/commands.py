import discord
from bot import Korii
from discord import app_commands
from discord.ext import commands
from utilities.subclasses import Embed


class CommandsCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    confessions = app_commands.Group(
        name="confessions", description="Commands to manage the confessions system."
    )

    @confessions.command(description="")
    @app_commands.guild_only()
    async def confess(self, interaction: discord.Interaction, confession: str):
        assert interaction.guild

        channel = await self.bot.pool.fetchval(
            "SELECT channel_id FROM confessions WHERE guild_id = $1",
            interaction.guild.id,
        )

        if not channel:
            embed = Embed(
                title="Confessions not setup properly",
                description="The confessions module has not been properly setup on this server.\n"
                "An administrator of this server must configure it using the `/settings confessions` command.",
            )
            embed.set_footer(
                text=f"If you think this is a mistake, use the `/support` command."
            )

            return await interaction.response.send_message(embed=embed)
