import sys
import time
from typing import List, Optional

import discord
import pkg_resources
import psutil
from discord import app_commands
from discord.ext import commands

from utils import utils, Embed, Interaction
from bot import Korii


class UserInfoView(discord.ui.View):
    def __init__(self, user: discord.Member, fetched_user: discord.User):
        super().__init__()
        self.user = user
        self.fetched_user = fetched_user

    @discord.ui.button(label="Avatar", style=discord.ButtonStyle.grey)
    async def avatar(self, interaction: Interaction, button: discord.ui.Button):
        embed = Embed(title=f"<:owo:1036761720447828030> {self.user.display_name}'s Avatar")

        embed.set_image(url=self.user.display_avatar)

        return await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Banner", style=discord.ButtonStyle.grey)
    async def banner(self, interaction: Interaction, button: discord.ui.Button):
        if not self.fetched_user or not self.fetched_user.banner:
            return await interaction.response.send_message(f"{self.user.display_name} doesn't have a banner.", ephemeral=True)

        embed = Embed(title=f"<:owo:1036761720447828030> {self.user.display_name}'s Banner")

        embed.set_image(url=self.fetched_user.banner.url)

        return await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🗑️", style=discord.ButtonStyle.red)
    async def delete(self, interaction: Interaction, button: discord.ui.Button):
        assert interaction.message

        await interaction.message.delete()
        return await interaction.response.send_message("hehe oki", ephemeral=True)


class InfoCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    async def format_permissions(self, permissions: discord.Permissions):
        staff_permissions = dict({x for x in permissions if x[1] is True} - set(discord.Permissions(521942715969)))

        formatted_permissions = []

        for x in staff_permissions:
            formatted_permissions.append(x.replace("_", " ").replace("guild", "server").replace("tts", "TTS").replace("log", "logs").title())

        if len(formatted_permissions) > 5:
            joined_permissions = ", ".join(formatted_permissions)
            new_lined_joined_permissions = "\n".join(formatted_permissions)
            return f"[`View permissions`]({await utils.shorten_text(self.bot, text=new_lined_joined_permissions)} '{await utils.shorten_text(self.bot, text=new_lined_joined_permissions, length=124, link=False)}...')"

        return ", ".join(f"`{x}`" for x in formatted_permissions)

    async def format_roles(self, roles: List[discord.Role]):
        formatted_roles = []

        for x in roles:
            formatted_roles.append(x.name)

        if len(formatted_roles) > 5:
            joined_roles = ", ".join(formatted_roles)
            new_lined_joined_roles = "\n".join(formatted_roles)
            return f"[`View roles`]({await utils.shorten_text(self.bot, text=new_lined_joined_roles)} '{await utils.shorten_text(self.bot, text=new_lined_joined_roles, length=124, link=False)}...')"

        return ", ".join(f"`{x}`" for x in formatted_roles)

    @app_commands.command(description="View information on the current server.")
    @app_commands.checks.cooldown(1, 5)
    async def server_info(self, interaction: Interaction):
        assert interaction.guild and interaction.guild.owner

        embed = Embed(title="Server Information")

        embed.add_field(
            name="Information",
            value=f"{self.bot.E['edit']} **Name:** {interaction.guild.name}\n"
            f"{self.bot.E['text2']} **ID:** `{interaction.guild.id}`\n"
            f"{self.bot.E['text1']} **Description:** {await utils.shorten_text(self.bot, interaction.guild.description or 'No description.', 16)}\n"
            "\n"
            f"{self.bot.E['owner']} **Owner:** {interaction.guild.owner.display_name}\n"
            f"{self.bot.E['text2']} **ID:** `{interaction.guild.owner.id}`\n"
            f"{self.bot.E['text1']} **Mention:** {interaction.guild.owner.mention}\n"
            f"\n"
            f"{self.bot.E['date']} **Created:** {discord.utils.format_dt(interaction.guild.created_at, style='R')}\n"
            f"{self.bot.E['text1']} **Full date:** {discord.utils.format_dt(interaction.guild.created_at, style='f')}",
        )

        embed.add_field(
            name="Numbers",
            value=f"{self.bot.E['text_channel']} **Channels:** `{len(interaction.guild.channels)}`\n"
            f"{self.bot.E['text2']} **Text:** `{len(interaction.guild.text_channels)}`\n"
            f"{self.bot.E['text2']} **Voice:** `{len(interaction.guild.voice_channels)}`\n"
            f"{self.bot.E['text1']} **Threads:** `{len(interaction.guild.threads)}`\n"
            "\n"
            f"{self.bot.E['people']} **Members:** `{interaction.guild.member_count}`\n"
            f"{self.bot.E['text2']} **Humans:** `{len([member for member in interaction.guild.members if not member.bot])}`\n"
            f"{self.bot.E['text1']} **Robots:** `{len([member for member in interaction.guild.members if member.bot])}`\n"
            "\n"
            f"{self.bot.E['roles']} **Roles:** {await self.format_roles([x for x in interaction.guild.roles if not x.is_default()])}\n"
            f"{self.bot.E['text1']} **Amount:** `{len(interaction.guild.roles)}`",
        )

        return await interaction.response.send_message(embed=embed)

    @app_commands.command(description="View information on the specified user.")
    @app_commands.checks.cooldown(1, 5)
    async def user_info(
        self,
        interaction: Interaction,
        user: Optional[discord.Member] = None,
    ):
        assert isinstance(interaction.user, discord.Member) and interaction.guild

        user = user or interaction.user
        user = interaction.guild.get_member(user.id)

        assert isinstance(user, discord.Member) and user.joined_at

        boosted = ""
        voice = ""

        status_emojis = {
            "online": self.bot.E["online"],
            "idle": self.bot.E["idle"],
            "dnd": self.bot.E["dnd"],
            "streaming": self.bot.E["streaming"],
            "offline": self.bot.E["offline"],
        }

        embed = Embed(
            title=f"{status_emojis[user.status.name]} User Information {'- hehe t-this me OwO' if user.id == interaction.guild.me.id else ''}"
        )

        if user.premium_since:
            boosted = (
                f"\n{self.bot.E['boost']} **Boosted:** {discord.utils.format_dt(user.premium_since, style='R')}\n"
                f"{self.bot.E['text1']} **Full date:** {discord.utils.format_dt(user.premium_since, style='f')}"
            )

        embed.add_field(
            name="General Information",
            value=f"{self.bot.E['edit']} **Name:** `{user.display_name}`\n"
            f"{self.bot.E['text2']} **ID:** `{user.id}`\n"
            f"{self.bot.E['text1']} **Tag:** `{user}`\n"
            f"\n"
            f"{self.bot.E['date']} **Created:** {discord.utils.format_dt(user.created_at, style='R')}\n"
            f"{self.bot.E['text1']} **Full date:** {discord.utils.format_dt(user.created_at, style='f')}\n"
            f"\n"
            f"{self.bot.E['date']} **Joined:** {discord.utils.format_dt(user.joined_at, style='R')}\n"
            f"{self.bot.E['text2']} **Position:** `{sorted(interaction.guild.members, key=lambda m: m.joined_at or discord.utils.utcnow()).index(user) + 1}`\n"
            f"{self.bot.E['text1']} **Full date:** {discord.utils.format_dt(user.joined_at, style='f')}",
        )

        if user.voice and user.voice.channel:
            users = len(user.voice.channel.members) - 1
            mute = user.voice.mute or user.voice.self_mute
            deaf = user.voice.deaf or user.voice.self_deaf
            video = user.voice.self_video

            voice = (
                f"\n{self.bot.E['stage_channel']} **Voice:** in {user.voice.channel.mention}\n"
                f"{self.bot.E['text2']} {f'with {users} others.' if users else f'by themselves.'}\n"
                f"{self.bot.E['text1']} {'Muted' if mute else 'Not muted'}, {'deafened' if deaf else 'not deafened'} and {'streaming' if video else 'not streaming'}.\n"
            )

        embed.add_field(
            name="Other Information",
            value=f"{self.bot.E['roles']} **Roles:** {await self.format_roles([x for x in user.roles if not x.is_default()])}\n"
            f"{self.bot.E['text2']} **Amount:** `{len([x for x in user.roles if not x.is_default()])}`\n"
            f"{self.bot.E['text2']} **Top Role:** `{user.top_role}`\n"
            f"{self.bot.E['text2']} **Color:** `{user.color}`\n"
            f"{self.bot.E['text1']} **Permissions:** {await self.format_permissions(user.guild_permissions)}\n"
            f"{voice}"
            f"{boosted}",
        )

        fetched_user = await self.bot.fetch_user(user.id)

        return await interaction.response.send_message(
            embed=embed,
            view=UserInfoView(user=user, fetched_user=fetched_user),
        )

    @app_commands.command(name="bot_info", description="View information about the bot.")
    @app_commands.checks.cooldown(1, 5)
    async def _bot_info(self, interaction: Interaction):
        github = "https://github.com/Korino-Development/Korii-Bot"
        invite = "https://bot.spooki.xyz"
        website = "https://spooki.xyz/bot"

        links = f"{self.bot.E['github']} [`Source`]({github}) | {self.bot.E['invite']} [`Invite`]({invite}) | {self.bot.E['globe']} [`Website`]({website})"

        users = [
            f"**Total:** `{len(self.bot.users):,}`",
            f"**Humans:** `{len([user for user in self.bot.users if not user.bot]):,}`",
            f"**Robots:** `{len([user for user in self.bot.users if user.bot]):,}`",
        ]

        total_channels = 0
        text_channels = 0
        voice_channels = 0

        for guild in self.bot.guilds:
            for channel in guild.channels:
                total_channels += 1
                if isinstance(channel, discord.TextChannel):
                    text_channels += 1

                elif isinstance(channel, discord.VoiceChannel):
                    voice_channels += 1

        channels = [
            f"**Total:** `{total_channels:,}`",
            f"**Text:** `{text_channels:,}`",
            f"**Voice:** `{voice_channels:,}`",
        ]

        system = [
            f"**CPU:** `{psutil.cpu_percent()}%`",
            f"**RAM:** `{psutil.virtual_memory().percent}%`",
            "`/neofetch` for more.",
        ]

        pool_start = time.perf_counter()
        await self.bot.pool.fetch("SELECT 1")
        pool_end = time.perf_counter()
        total_pool = (pool_end - pool_start) * 1000

        pings = [
            f"**Websocket:** `{round(self.bot.latency * 1000, 2)}ms`",
            f"**Database:** `{round(total_pool, 2)}ms`",
            "`/ping` for more.",
        ]

        code = [
            f"**Lines:** `{self.bot.lines:,}`",
            f"**Classes:** `{self.bot.classes:,}`",
            f"**Functions:** `{self.bot.functions:,}`",
        ]

        postgresql_version = await self.bot.pool.fetchval("SELECT VERSION();")

        versions = [
            f"**Python:** `{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}`",
            f"**discord.py:** `{pkg_resources.get_distribution('discord.py').version}`",
            f"**PostgreSQL:** `{postgresql_version.split()[1]}`",
        ]

        embed = Embed(description=f"{links}\n_ _╰ Try `/source <command>`\n\n** Latest Commits**\n{utils.get_latest_commits()}")
        embed.add_field(name="Users", value="\n".join(users))
        embed.add_field(name="Channels", value="\n".join(channels))
        embed.add_field(name="Code", value="\n".join(code))
        embed.add_field(name="System", value="\n".join(system))
        embed.add_field(name="Pings", value="\n".join(pings))
        embed.add_field(name="Versions", value="\n".join(versions))
        embed.set_footer(text="Thank you for choosing Korii 💖")

        return await interaction.response.send_message(embed=embed)
