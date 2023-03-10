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

import contextlib
from typing import Optional

import discord
from bot import Korii, Embed, Interaction
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands


class BasicCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @app_commands.command(description="Kicks the specified member from the server.")
    @app_commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.describe(member="The member to kick.")
    @app_commands.describe(reason="The reason we are kicking this member.")
    @app_commands.describe(
        silent="If we should send the kick message privately meaning only you can see it."
    )
    @app_commands.describe(notify="If we should DM the user before we kick them.")
    async def kick(
        self,
        interaction: Interaction,
        member: discord.Member,
        reason: Optional[str],
        silent: bool = False,
        notify: bool = False,
    ):
        assert interaction.guild

        notified = False

        if notify:
            with contextlib.suppress(discord.HTTPException, discord.Forbidden):
                embed = Embed(
                    title=f"{self.bot.E['hammer']} You have been kicked!",
                    description=f"{self.bot.E['user']} **User:** {member}\n"
                    f"{self.bot.E['shield']} **Guild:** {interaction.guild.name}\n"
                    f"{self.bot.E['question']} **Reason:** {reason}",
                    color=discord.Color.orange(),
                    executed=interaction.user.display_name,
                )

                notified = True
                await member.send(embed=embed)

        embed = Embed(
            title=f"{self.bot.E['hammer']} Kicked {member.display_name}",
            color=discord.Color.orange(),
            executed=f"{interaction.user.display_name} | Notified: {self.bot.yn(notified)}",
        )

        embed.add_field(
            name=f"{self.bot.E['question']} Reason",
            value=reason if reason else "No reason provided.",
        )

        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embed, ephemeral=silent)

    @app_commands.command(description="Ban the specified member from the server.")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(member="The member to ban.")
    @app_commands.describe(reason="The reason we are banning this member.")
    @app_commands.describe(
        delete_messages="How much of their recent message history we should delete. Must be between 0 and 7."
    )
    @app_commands.describe(
        silent="If we should send the ban message privately meaning only you can see it."
    )
    @app_commands.describe(
        soft="If we should we instantly unban the member. This deletes the previous messages if specified."
    )
    @app_commands.describe(notify="If we should DM the user before we ban them.")
    @app_commands.choices(
        delete_messages=[
            Choice(name="Past 24 hours", value=1),
            Choice(name="Past 2 days", value=2),
            Choice(name="Past 3 days", value=3),
            Choice(name="Past 4 days", value=4),
            Choice(name="Past 5 days", value=5),
            Choice(name="Past 6 days", value=6),
            Choice(name="Past week", value=7),
        ]
    )
    async def ban(
        self,
        interaction: Interaction,
        member: discord.Member,
        delete_messages: Choice[int],
        reason: Optional[str] = "No reason provided.",
        silent: bool = False,
        soft: bool = False,
        notify: bool = False,
    ):
        assert interaction.guild

        notified = False

        if notify:
            with contextlib.suppress(discord.HTTPException, discord.Forbidden):
                embed = Embed(
                    title=f"{self.bot.E['hammer']} You have been banned!",
                    description=f"{self.bot.E['user']} **User:** {member}\n"
                    f"{self.bot.E['shield']} **Guild:** {interaction.guild.name}\n"
                    f"{self.bot.E['question']} **Reason:** {reason}",
                    color=discord.Color.red(),
                    executed=f"{interaction.user.display_name} | Soft: {self.bot.yn(soft)}",
                )

                notified = True
                await member.send(embed=embed)

        await interaction.guild.ban(
            member, reason=reason, delete_message_days=delete_messages.value
        )

        if soft:
            await interaction.guild.unban(member, reason=reason)

        embed = Embed(
            title=f"{self.bot.E['hammer']} Banned {member.display_name}",
            color=discord.Color.red(),
            executed=f"{interaction.user.display_name} | Soft: {self.bot.yn(soft)} | Notified: {self.bot.yn(notified)}",
        )

        embed.add_field(name=f"{self.bot.E['question']} Reason", value=reason)
        embed.add_field(name="Delete messages", value=delete_messages.name)

        return await interaction.response.send_message(embed=embed, ephemeral=silent)

    @app_commands.command(description="Unban the specified member from the server.")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(user="The user to unban.")
    @app_commands.describe(reason="The reason we are unbanning this user.")
    @app_commands.describe(
        silent="If we should send the unban message privately meaning only you can see it."
    )
    async def unban(
        self,
        interaction: Interaction,
        user: discord.User,
        reason: Optional[str] = "No reason provided.",
        silent: bool = False,
    ):
        assert interaction.guild

        await interaction.guild.unban(user, reason=reason)

        embed = Embed(
            title=f"{self.bot.E['hammer']} Unbanned {user}",
            color=discord.Color.red(),
            executed=interaction.user.display_name,
        )

        embed.add_field(name=f"{self.bot.E['question']} Reason", value=reason)

        return await interaction.response.send_message(embed=embed, ephemeral=silent)
