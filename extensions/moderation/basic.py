import contextlib
from typing import Optional

import discord
from discord import app_commands
from discord.app_commands import Choice

from utils import Embed, Interaction, utils

from ._base import ModerationBase


class BasicCog(ModerationBase):
    @app_commands.command(description="Kicks the specified member from the server.")
    @app_commands.guild_only()
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.describe(member="The member to kick.")
    @app_commands.describe(reason="The reason we are kicking this member.")
    @app_commands.describe(silent="If we should send the kick message privately meaning only you can see it.")
    @app_commands.describe(notify="If we should DM the user before we kick them.")
    async def kick(
        self,
        interaction: Interaction,
        member: discord.Member,
        reason: Optional[str] = "No reason provided.",
        silent: bool = False,
        notify: bool = False,
    ):
        assert interaction.guild

        notified = False

        if notify:
            with contextlib.suppress(discord.HTTPException, discord.Forbidden):
                embed = Embed(
                    title=f"🛠️ You have been kicked!",
                    description=f"💁 **User:** {member} \n🛡️ **Guild:** {interaction.guild.name} \n❓ **Reason:** {reason}",
                    color=discord.Color.orange(),
                    executed=interaction.user.display_name,
                )

                notified = True
                await member.send(embed=embed)

        embed = Embed(
            title=f"🛠️ Kicked {member.display_name}",
            color=discord.Color.orange(),
            executed=f"{interaction.user.display_name} | Notified: {utils.yn(notified)}",
        )

        embed.add_field(
            name=f"❓ Reason",
            value=reason if reason else "No reason provided.",
        )

        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embed, ephemeral=silent)

    @app_commands.command(description="Ban the specified member from the server.")
    @app_commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(member="The member to ban.")
    @app_commands.describe(reason="The reason we are banning this member.")
    @app_commands.describe(delete_messages="How much of their recent message history we should delete. Must be between 0 and 7.")
    @app_commands.describe(silent="If we should send the ban message privately meaning only you can see it.")
    @app_commands.describe(soft="If we should we instantly unban the member. This deletes the previous messages if specified.")
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
                    title=f"🛠️ You have been banned!",
                    description=f"💁 **User:** {member} \n🛡️ **Guild:** {interaction.guild.name} \n❓ **Reason:** {reason}",
                    color=discord.Color.red(),
                    executed=f"{interaction.user.display_name} | Soft: {utils.yn(soft)}",
                )

                notified = True
                await member.send(embed=embed)

        await interaction.guild.ban(member, reason=reason, delete_message_days=delete_messages.value)

        if soft:
            await interaction.guild.unban(member, reason=reason)

        embed = Embed(
            title=f"🛠️ Banned {member.display_name}",
            color=discord.Color.red(),
            executed=f"{interaction.user.display_name} | Soft: {utils.yn(soft)} | Notified: {utils.yn(notified)}",
        )

        embed.add_field(name=f"❓ Reason", value=reason)
        embed.add_field(name="Delete messages", value=delete_messages.name)

        return await interaction.response.send_message(embed=embed, ephemeral=silent)

    @app_commands.command(description="Unban the specified member from the server.")
    @app_commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.describe(user="The user to unban.")
    @app_commands.describe(reason="The reason we are unbanning this user.")
    @app_commands.describe(silent="If we should send the unban message privately meaning only you can see it.")
    async def unban(self, interaction: Interaction, user: discord.User, reason: Optional[str] = "No reason provided.", silent: bool = False):
        assert interaction.guild

        await interaction.guild.unban(user, reason=reason)

        embed = Embed(
            title=f"🛠️ Unbanned {user}",
            color=discord.Color.red(),
            executed=interaction.user.display_name,
        )

        embed.add_field(name=f"❓ Reason", value=reason)

        return await interaction.response.send_message(embed=embed, ephemeral=silent)
