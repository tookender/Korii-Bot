import traceback, random
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from utils import Embed, Interaction, Invalid, constants

from ._base import ConfigBase


class Modal(discord.ui.Modal):
    def __init__(self):
        super().__init__()

    async def update_database(self, interaction: Interaction):
        return

    async def on_error(self, interaction: Interaction, error: Exception):
        if isinstance(error, Invalid):
            return await interaction.response.send_message(str(error), ephemeral=True)

    async def on_submit(self, interaction: Interaction):
        await self.update_database(interaction)
        return await update_message(interaction)


class MessageModal(Modal, title="Config: Levelling"):
    message = discord.ui.TextInput(
        label="Announcement Message",
        placeholder="Variables: {user} {user_mention} {level} {next_level} {guild}",
    )

    async def update_database(self, interaction: Interaction):
        assert interaction.guild
        return await interaction.client.pool.execute(
            "UPDATE guilds SET levelling_message = $1 WHERE guild_id = $2", self.message.value, interaction.guild.id
        )


class LevellingChannelView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.select(
        cls=discord.ui.ChannelSelect,
        placeholder="Select an announcement channel...",
        max_values=1,
        min_values=1,
        channel_types=[
            discord.ChannelType.text,
            discord.ChannelType.news,
            discord.ChannelType.voice,
            discord.ChannelType.private_thread,
            discord.ChannelType.public_thread,
        ],
    )
    async def select_channel(self, interaction: Interaction, select: discord.ui.ChannelSelect):
        assert interaction.guild and isinstance(interaction.user, discord.Member)
        channel = interaction.guild.get_channel_or_thread(select.values[0].id)
        assert isinstance(channel, discord.abc.Messageable)

        if not channel.permissions_for(interaction.user).send_messages:
            return await interaction.response.send_message("You can't send messages in that channel.", ephemeral=True)

        await interaction.client.pool.execute("UPDATE guilds SET levelling_channel = $1 WHERE guild_id = $2", channel.id, interaction.guild.id)
        return await update_message(interaction)


class XPMultiplierModal(Modal, title="Config: Levelling"):
    multiplier = discord.ui.TextInput(
        label="XP Multiplier",
        placeholder="Multiplier of XP. Default is 1.0",
    )

    async def update_database(self, interaction: Interaction):
        assert interaction.guild
        multiplier = float(self.multiplier.value)

        if not multiplier or not isinstance(multiplier, float):
            raise Invalid("Invalid multiplier. Must be a float (e.g. 2.0, 1.5, etc)")

        await interaction.client.pool.execute("UPDATE guilds SET levelling_multiplier = $1 WHERE guild_id = $2", multiplier, interaction.guild.id)
        return await update_message(interaction)


class ConfigLevellingDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Enable/Disable Levelling", description="Enable or disable levelling.", emoji="⚡"),
            discord.SelectOption(label="Enable/Disable Announcements", description="Change if we should send a level-up message.", emoji="📢"),
            discord.SelectOption(
                label="Change Announcement Channel", description="Change where the message that is sent once you level-up.", emoji="#️⃣"
            ),
            discord.SelectOption(label="Change Announcement Message", description="Change the message that is sent once you level-up.", emoji="💬"),
            discord.SelectOption(label="Change XP Multiplier", description="Change the XP multiplier. Default is 1.0.", emoji="🏆"),
        ]

        super().__init__(placeholder="Change an option...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if interaction.guild:
            data = await interaction.client.pool.fetchrow(
                "SELECT levelling_enabled, levelling_announce, levelling_multiplier FROM guilds WHERE guild_id = $1", interaction.guild.id
            )

            match self.values[0]:
                case "Enable/Disable Levelling":
                    await interaction.client.pool.execute(
                        "UPDATE guilds SET levelling_enabled = $1 WHERE guild_id = $2", False if data[0] else True, interaction.guild.id
                    )
                case "Enable/Disable Announcements":
                    await interaction.client.pool.execute(
                        "UPDATE guilds SET levelling_announce = $1 WHERE guild_id = $2", False if data[1] else True, interaction.guild.id
                    )
                case "Change Announcement Channel":
                    return await interaction.response.send_message(view=LevellingChannelView(), ephemeral=True)
                case "Change Announcement Message":
                    return await interaction.response.send_modal(MessageModal())
                case "Change XP Multiplier":
                    return await interaction.response.send_modal(XPMultiplierModal())

            return await update_message(interaction)


class ConfigLevelling(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author
        self.add_item(ConfigLevellingDropdown())
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id == self.author.id:
            return True

        message = random.choice(constants.NOT_YOUR_BUTTON)
        await interaction.response.send_message(message.replace("[user]", self.author.display_name), ephemeral=True)
        return False

    @discord.ui.button(label="View Announcement Message", emoji="💬", style=discord.ButtonStyle.blurple)
    async def view_message(self, interaction: Interaction, button: discord.ui.Button):
        if interaction.guild:
            message = await interaction.client.pool.fetchval("SELECT levelling_message FROM guilds WHERE guild_id = $1", interaction.guild.id)

            if not message:
                return await interaction.response.send_message(
                    "No announcement message has been found. Use the dropdown to change it.", ephemeral=True
                )

            return await interaction.response.send_message(f"**Announcement Message:** `{message}`", ephemeral=True)


async def update_message(interaction: Interaction, edit: Optional[bool] = True):
    try:
        if interaction.guild:
            data = await interaction.client.pool.fetchrow(
                "SELECT levelling_enabled, levelling_announce, levelling_channel, levelling_message, levelling_multiplier FROM guilds WHERE guild_id = $1",
                interaction.guild.id,
            )

            if not data:
                await interaction.client.pool.execute("INSERT INTO guilds(guild_id) VALUES ($1)", interaction.guild.id)
                await update_message(interaction, edit)

            bool_emojis = {
                True: "🟩",
                False: "🟥",
                None: "⬜",
            }

            embed = Embed(
                title="Config: Levelling",
                description="`🟩 Enabled`\n"
                "`🟥 Disabled`\n"
                "`⬜ Not set`\n\n"
                f"```\n"
                f"Enabled              - {bool_emojis[data[0]]}\n"
                f"Announce             - {bool_emojis[data[1]]}\n"
                f"Announcement Channel - {interaction.guild.get_channel(data[2]) if data[2] else bool_emojis[data[2]] + ' direct'}\n"
                f"Announcement Message - {bool_emojis[True] + ' view below' if data[3] else bool_emojis[None]}\n"
                f"Banned Roles         - soon™\n"
                f"XP Multiplier        - {data[4]}\n"
                f"```",
            )

            if not edit:
                return await interaction.response.send_message(embed=embed, view=ConfigLevelling(author=interaction.user))

            return await interaction.response.edit_message(embed=embed, view=ConfigLevelling(author=interaction.user))

    except Exception as e:
        return await interaction.response.send_message(f"An error occurred: {traceback.format_exception(e)}", ephemeral=True)


class LevellingConfig(ConfigBase):
    @app_commands.command(description="Configure your guild's levelling system.")
    async def levelling_config(self, interaction: Interaction):
        return await update_message(interaction, edit=False)

    @commands.command(name="levelling_config", description="Please use the slash command /levelling_config", aliases=["level_config", "levelling"])
    async def levelling_config2(self, ctx):
        return await ctx.send("⚠️ | This command is deprecated, please use the /levelling_config slash command.")