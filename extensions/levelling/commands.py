import math
from typing import Optional

import discord
from discord import app_commands

from utils import Embed, Interaction

from ._base import LevellingBase


class CommandsCog(LevellingBase):
    @app_commands.command(description="View the level of the specified member.")
    @app_commands.describe(user="The user you want to view the level of.")
    @app_commands.guild_only()
    async def level(self, interaction: Interaction, user: Optional[discord.Member] = None):
        if not interaction.guild or isinstance(interaction.user, discord.User):
            return

        guild_levelling = await self.bot.pool.fetchval("SELECT levelling_enabled FROM guilds WHERE guild_id = $1", interaction.guild.id)

        if not guild_levelling:
            embed = Embed(
                title="⚡ | Levelling disabled!",
                description="This guild has levelling disabled, to enable it use the `/config levelling` command.",
            )

            return await interaction.response.send_message(embed=embed)

        user = user if user else interaction.user

        data = await self.bot.pool.fetchrow(
            "SELECT level, xp FROM levels WHERE guild_id = $1 AND user_id = $2",
            interaction.guild.id,
            user.id,
        )

        if not data:
            await self.bot.pool.execute(
                "INSERT INTO levels (guild_id, user_id, level, xp) VALUES ($1, $2, $3, $4)",
                interaction.guild.id,
                user.id,
                0,
                0,
            )
            embed = Embed(
                title="⚡ | No messages!",
                description=f"{'You have' if interaction.user.id == user.id else f'{user.display_name} has' } not sent any messages in this server.",
            )

            return await interaction.response.send_message(embed=embed)

        ap = "'"

        embed = Embed(
            title=f"⚡ | {'Your' if interaction.user.id == user.id else f'{user.display_name}{ap}s'} level",
            description=f"**Level:** `{data[0]}`\n" f"**XP:** `{data[1]} / {math.floor(10 * (data[0] ^ 2) + (55 * data[0]) + 100)}`",
        )

        return await interaction.response.send_message(embed=embed)
