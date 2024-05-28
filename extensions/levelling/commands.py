import math
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import Embed, Interaction

from ._base import LevellingBase


class CommandsCog(LevellingBase):
    @commands.hybrid_command(description="View the level of the specified member.")
    @app_commands.describe(user="The user you want to view the level of.")
    @app_commands.guild_only()
    async def level(self, ctx, user: Optional[discord.Member] = None):
        if not ctx.guild or isinstance(ctx.author, discord.User):
            return

        guild_levelling = await self.bot.pool.fetchval("SELECT levelling_enabled FROM guilds WHERE guild_id = $1", ctx.guild.id)

        if not guild_levelling:
            embed = Embed(
                description=f"{self.bot.E['no']} This guild has levelling disabled, to enable it use the `/config levelling` command.",
            )

            embed.set_author(
                name=ctx.author.global_name,
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
            )

            return await ctx.send(embed=embed)

        user = user if user else ctx.author

        data = await self.bot.pool.fetchrow(
            "SELECT level, xp FROM levels WHERE guild_id = $1 AND user_id = $2",
            ctx.guild.id,
            user.id,
        )

        if not data:
            await self.bot.pool.execute(
                "INSERT INTO levels (guild_id, user_id, level, xp) VALUES ($1, $2, $3, $4)",
                ctx.guild.id,
                user.id,
                0,
                0,
            )

            q = "'"

            embed = Embed(
                description=f"{self.bot.E['no']} {f'You don{q}t have' if ctx.user.id == user.id else f'{user.display_name} doesn{q}t has'} a level yet. Try sending more messages.",
            )

            embed.set_author(
                name=user.global_name,
                icon_url=user.avatar.url if user.avatar else None,
            )

            return await ctx.send(embed=embed)

        embed = Embed(
            description=f"**Level:** `{data[0]}`\n" f"**XP:** `{data[1]} / {math.floor(10 * (data[0] ^ 2) + (55 * data[0]) + 100)}`",
        )

        embed.set_author(
            name=user.global_name,
            icon_url=user.avatar.url if user.avatar else None,
        )

        return await ctx.send(embed=embed)
