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

import traceback
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from bot import Embed, Interaction


class ConfigLevellingMessageModal(discord.ui.Modal, title="Config: Levelling"):
    message = discord.ui.TextInput(
        label="Announcement Message",
        placeholder="Variables: {user} {user_mention} {level} {next_level} {guild}",
    )
    
    async def on_submit(self, interaction: Interaction):
        if interaction.guild:
            await interaction.client.pool.execute("UPDATE guilds SET levelling_message = $1 WHERE guild_id = $2", self.message.value, interaction.guild.id)
            return await update_message(interaction)
    
    async def on_error(self, interaction: Interaction, error: Exception):
        return await interaction.response.send_message(f"Something fucked up: {error}", ephemeral=True)


class ConfigLevellingChannelModal(discord.ui.Modal, title="Config: Levelling"):
    channel = discord.ui.TextInput(
        label="Announcement Channel ID",
        placeholder="ID of your announcements channel...",
    )
    
    async def on_submit(self, interaction: Interaction):
        if interaction.guild:
            channel = interaction.guild.get_channel(int(self.channel.value))

            if not channel:
                return await interaction.response.send_message("Invalid channel ID.", ephemeral=True)

            if not isinstance(channel, discord.TextChannel):
                return await interaction.response.send_message("Channel must be a text channel.", ephemeral=True)

            await interaction.client.pool.execute("UPDATE guilds SET levelling_channel = $1 WHERE guild_id = $2", channel.id, interaction.guild.id)
            return await update_message(interaction)
    
    async def on_error(self, interaction: Interaction, error: Exception):
        return await interaction.response.send_message(f"Something fucked up: {error}", ephemeral=True)


class ConfigLevellingDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Enable/Disable Levelling", description="Enable or disable levelling.", emoji="⚡"),
            discord.SelectOption(label="Enable/Disable Announcements", description="Change if we should send a level-up message.", emoji="📢"),
            discord.SelectOption(label="Change Announcement Channel", description="Change where the message that is sent once you level-up.", emoji="#️⃣"),
            discord.SelectOption(label="Change Announcement Message", description="Change the message that is sent once you level-up.", emoji="💬"),
            discord.SelectOption(label="Enable/Disable Double XP", description="Enable or disable double XP.", emoji="🏆"),
        ]

        super().__init__(placeholder="Change an option...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if interaction.guild:
            data = await interaction.client.pool.fetchrow("SELECT levelling_enabled, levelling_announce, levelling_double_xp FROM guilds WHERE guild_id = $1", interaction.guild.id)

            match self.values[0]:
                case "Enable/Disable Levelling":
                    await interaction.client.pool.execute("UPDATE guilds SET levelling_enabled = $1 WHERE guild_id = $2", False if data[0] else True, interaction.guild.id)
                case "Enable/Disable Announcements":
                    await interaction.client.pool.execute("UPDATE guilds SET levelling_announce = $1 WHERE guild_id = $2", False if data[1] else True, interaction.guild.id)
                case "Change Announcement Channel":
                    return await interaction.response.send_modal(ConfigLevellingChannelModal())
                case "Change Announcement Message":
                    return await interaction.response.send_modal(ConfigLevellingMessageModal())
                case "Enable/Disable Double XP":
                    await interaction.client.pool.execute("UPDATE guilds SET levelling_double_xp = $1 WHERE guild_id = $2", False if data[2] else True, interaction.guild.id)
                    
            return await update_message(interaction)


class ConfigLevelling(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ConfigLevellingDropdown())

    @discord.ui.button(label="View Announcement Message", emoji="💬", style=discord.ButtonStyle.blurple)
    async def view_message(self, interaction: Interaction, button: discord.ui.Button):
        if interaction.guild:
            message = await interaction.client.pool.fetchval("SELECT levelling_message FROM guilds WHERE guild_id = $1", interaction.guild.id)
            
            if not message:
                return await interaction.response.send_message("No announcement message has been found. Use the dropdown to change it.", ephemeral=True)

            return await interaction.response.send_message(f"**Announcement Message:** `{message}`", ephemeral=True)


async def update_message(interaction: Interaction, edit: Optional[bool] = True):
    try:
        if interaction.guild:
            data = await interaction.client.pool.fetchrow("SELECT levelling_enabled, levelling_announce, levelling_channel, levelling_message, levelling_double_xp FROM guilds WHERE guild_id = $1", interaction.guild.id)

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
                            f"Double XP            - {bool_emojis[data[4]]}\n"
                            f"```",
            )

            if not edit:
                return await interaction.response.send_message(embed=embed, view=ConfigLevelling())

            return await interaction.response.edit_message(embed=embed, view=ConfigLevelling())
        
    except Exception as e:
        return await interaction.response.send_message(f"An error occurred: {traceback.format_exception(e)}", ephemeral=True)


class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    group = app_commands.Group(name="config", description="Configure your guild's bot configuration.")
    
    @group.command(description="Configure your guild's levelling system.")
    async def levelling(self, interaction: Interaction):
        return await update_message(interaction, edit=False)
