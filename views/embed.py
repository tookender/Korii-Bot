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

import re
from typing import Type, List

import discord

from utils import Interaction

nl = "\n"
URL_REGEX = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
MESSAGE_REGEX = re.compile(
    r"(?:https://)?(?:[a-zA-Z_]*.)?discord.com/channels/(?P<guild>[0-9]*)/(?P<channel>[0-9]*)/(?P<message>[0-9]*)"
)


class Modal(discord.ui.Modal):
    def __init__(self, embed: discord.Embed):
        self.embed = embed
        self.update_defaults(embed)
        super().__init__()

    def update_defaults(self, embed: discord.Embed):
        return


class EditEmbedModal(Modal, title="Edit Embed"):
    _title = discord.ui.TextInput(label="Embed Title", placeholder="Leave any field empty to remove its content", max_length=256, required=False)
    description = discord.ui.TextInput(label="Embed Description", placeholder="This can be up to 4,000 characters long", style=discord.TextStyle.long, required=False)
    image = discord.ui.TextInput(label="Embed Image URL", placeholder="Must be in a HTTP(S) format", required=False)
    thumbnail = discord.ui.TextInput(label="Embed Thumbnail Image URL", placeholder="Must also be in HTTP(S) format", required=False)
    color = discord.ui.TextInput(label="Embed Color", placeholder="Formats: Hex [#00000] or RGB (rgb(num, num, num))", required=False)

    def update_defaults(self, embed: discord.Embed):
        self._title.default = embed.title
        self.description.default = embed.description
        self.image.default = embed.image.url
        self.thumbnail.default = embed.thumbnail.url
        if embed.color:
            self.color.default = str(embed.color)

    async def on_submit(self, interaction: Interaction):
        failed = []

        embed = self.embed.copy()
        embed.title = self._title.value.strip() or None
        embed.description = self.description.value.strip() or None

        if URL_REGEX.fullmatch(self.image.value):
            embed.set_image(url=self.image.value)
        elif self.image.value:
            failed.append("Image URL was invalid. Must follow the HTTP(S) format.")
        else:
            embed.set_image(url=None)

        if URL_REGEX.fullmatch(self.thumbnail.value):
            embed.set_thumbnail(url=self.thumbnail.value)
        elif self.thumbnail.value:
            failed.append("Thumbnail URL was invalid. Must follow the HTTP(S) format.")
        else:
            embed.set_thumbnail(url=None)

        if self.color.value:
            try:
                color = discord.Color.from_str(self.color.value)
                embed.color = color
            except Exception as e:
                failed.append("Color was invalid. Must follow the HEX (#fffff) or the RGB (rgb(num, num, num)) format.")
        else:
            embed.color = None

        self.update_defaults(embed)
        await interaction.response.edit_message(embed=embed)

        if failed:
            return await interaction.followup.send(f"**Failed:** {nl.join(failed)}", ephemeral=True)
        

class EditAuthorModal(Modal, title="Edit Embed Author"):
    name = discord.ui.TextInput(label="Author Name", placeholder="Leave any field empty to remove its content", max_length=256, required=False)
    url = discord.ui.TextInput(label="Author URL", placeholder="Must be in a HTTP(S) format", required=False)
    icon = discord.ui.TextInput(label="Author Icon URL", placeholder="Must also be in HTTP(S) format", required=False)

    def update_defaults(self, embed: discord.Embed):
        self.name.default = embed.author.name
        self.url.default = embed.author.url
        self.icon.default = embed.author.icon_url

    async def on_submit(self, interaction: Interaction):
        failed = []

        embed = self.embed.copy()

        if URL_REGEX.fullmatch(self.url.value):
            if not self.name.value:
                failed.append("Cannot add URL. Name is required to add an author.")
        elif self.url.value:
            if not self.name.value:
                failed.append("Cannot add URL. Name is required to add an author.")
            failed.append("Author URL was invalid. Must follow the HTTP(S) format.")

        if URL_REGEX.fullmatch(self.icon.value):
            if not self.name.value:
                failed.append("Cannot add Icon. Name is required to add an author.")
        elif self.icon.value:
            if not self.name.value:
                failed.append("Cannot add Icon. Name is required to add an author.")
            failed.append("Author Icon URL was invalid. Must follow the HTTP(S) format.")
        
        if self.name.value:
            embed.set_author(name=self.name.value, url=self.url.value, icon_url=self.icon.value)

        self.update_defaults(embed)
        await interaction.response.edit_message(embed=embed)

        if failed:
            return await interaction.followup.send(f"**Failed:** {nl.join(failed)}", ephemeral=True)


class EditFooterModal(Modal, title="Edit Embed Footer"):
    text = discord.ui.TextInput(label="Footer Text", placeholder="Leave any field empty to remove its content", max_length=256, required=False)
    icon = discord.ui.TextInput(label="Footer Icon URL", placeholder="Must also be in HTTP(S) format", required=False)

    def update_defaults(self, embed: discord.Embed):
        self.text.default = embed.footer.text
        self.icon.default = embed.footer.icon_url

    async def on_submit(self, interaction: Interaction):
        failed = []

        embed = self.embed.copy()

        if URL_REGEX.fullmatch(self.icon.value):
            if not self.text.value:
                failed.append("Cannot add URL. Text is required to add a footer.")
        elif self.icon.value:
            if not self.text.value:
                failed.append("Cannot add URL. Text is required to add a footer..")
            failed.append("Icon URL was invalid. Must follow the HTTP(S) format.")

        if self.text.value:
            embed.set_footer(text=self.text.value, icon_url=self.icon.value)

        self.update_defaults(embed)
        await interaction.response.edit_message(embed=embed)

        if failed:
            return await interaction.followup.send(f"**Failed:** {nl.join(failed)}", ephemeral=True)


class GetEmbedModal(Modal, title="Copy Embed"):
    message = discord.ui.TextInput(label="Message Link", placeholder="The link of the message featuring the embed (right click -> copy message link)", required=True)

    def update_defaults(self, embed: discord.Embed):
        return

    async def on_submit(self, interaction: Interaction):
        match = MESSAGE_REGEX.fullmatch(self.message.value)

        if not match:
            return await interaction.response.send_message("Invalid Message Link. Must follow this format: `https://discord.com/channels/guild_id/channel_id/message_id`")

        guild = interaction.client.get_guild(int(match['guild']))
        if not guild:
            return await interaction.response.send_message("Invalid guild ID.")

        channel = guild.get_channel(int(match['channel']))
        if not channel or not isinstance(channel, discord.TextChannel):
            return await interaction.response.send_message("Invalid channel ID.")
        

        message = channel.get_partial_message(int(match['message']))
        if not message:
            return await interaction.response.send_message("Invalid message ID.")
        
        message = await channel.fetch_message(message.id)
        embed = message.embeds[0]

        return await interaction.response.edit_message(embed=embed)

class ModalButton(discord.ui.Button):
    def __init__(self, modal: Type[Modal], **kwargs):
        self.modal = modal
        super().__init__(**kwargs)

    async def callback(self, interaction: Interaction):
        assert interaction.message and interaction.message.embeds
        return await interaction.response.send_modal(self.modal(interaction.message.embeds[0]))


class SendButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Send", style=discord.ButtonStyle.green, row=2)

    async def callback(self, interaction: Interaction):
        if not interaction.message:
            return await interaction.response.send_message("No message was found. Try again.", ephemeral=True)
        
        if not interaction.channel or not isinstance(interaction.channel, discord.TextChannel):
            return await interaction.response.send_message("No channel was found. Try again.", ephemeral=True)

        await interaction.message.delete()
        await interaction.channel.send(embed=interaction.message.embeds[0])
        await interaction.response.send_message(f"Embed has been sent.", ephemeral=True)


class SendToView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.select(cls=discord.ui.ChannelSelect, placeholder="Select a channel...", max_values=1, min_values=1, channel_types=[discord.ChannelType.text])
    async def select_channel(self, interaction: Interaction, select: discord.ui.ChannelSelect):
        if not interaction.guild:
            return await interaction.response.send_message("No guild was found. Try again.", ephemeral=True)

        if not interaction.message or not interaction.message.embeds:
            return await interaction.response.send_message("No message was found. Try again.", ephemeral=True)

        embed = interaction.message.embeds[0]
        await interaction.message.delete()
        for channel in select.values:
            channel = interaction.guild.get_channel(channel.id)

            if not isinstance(channel, discord.TextChannel):
                return await interaction.response.send_message("Invalid channel. Try again.", ephemeral=True)

            await channel.send(embed=embed)
            return await interaction.response.send_message(f"Embed was sent to {channel.mention}", ephemeral=True)


class SendToButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Send To", style=discord.ButtonStyle.green, row=2)

    async def callback(self, interaction: Interaction):
        if not interaction.message:
            return await interaction.response.send_message("No message was found. Try again.")

        return await interaction.response.edit_message(embed=interaction.message.embeds[0], view=SendToView())


class EmbedView(discord.ui.View):
    def __init__(self, author: discord.User | discord.Member):
        self.author = author
        super().__init__(timeout=360)
        self.add_items()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user == self.author:
            return True

        await interaction.response.send_message("Only the person that used the command can use this, sucks to suck.", ephemeral=True)
        return False

    def add_items(self):
        # Row 0
        self.add_item(discord.ui.Button(label="Edit:", style=discord.ButtonStyle.gray, disabled=True, row=0))
        self.add_item(ModalButton(EditEmbedModal, label="Embed", style=discord.ButtonStyle.blurple, row=0))
        self.add_item(ModalButton(EditAuthorModal, label="Author", style=discord.ButtonStyle.blurple, row=0))
        self.add_item(ModalButton(EditFooterModal, label="Footer", style=discord.ButtonStyle.blurple, row=0))

        # Row 1
        self.add_item(discord.ui.Button(label="Fields:", style=discord.ButtonStyle.gray, disabled=True, row=1))
        self.add_item(ModalButton(EditEmbedModal, emoji="➕", style=discord.ButtonStyle.green, row=1))  # Soon
        self.add_item(ModalButton(EditAuthorModal, emoji="➖", style=discord.ButtonStyle.red, row=1))  # Soon
        self.add_item(ModalButton(EditFooterModal, emoji="✏️", style=discord.ButtonStyle.blurple, row=1))  # Soon

        # Row 2
        self.add_item(SendButton())
        self.add_item(SendToButton())
        self.add_item(ModalButton(GetEmbedModal, label="Copy Embed", style=discord.ButtonStyle.green, row=2))
    
        # Row 3
        self.add_item(discord.ui.Button(label="0/6,000 Characters", style=discord.ButtonStyle.gray, disabled=True, row=3)) # Soon
        self.add_item(discord.ui.Button(label="0/25 Fields", style=discord.ButtonStyle.gray, disabled=True, row=3)) # Soon
