import re
from copy import deepcopy
from typing import List, Type

import discord

from utils import Interaction, utils

nl = "\n"
URL_REGEX = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
MESSAGE_REGEX = re.compile(r"(?:https://)?(?:[a-zA-Z_]*.)?discord.com/channels/(?P<guild>[0-9]*)/(?P<channel>[0-9]*)/(?P<message>[0-9]*)")


class Invalid(Exception): ...


class EmbedView(discord.ui.View):
    def __init__(self, author: discord.User | discord.Member):
        self.author = author
        self.embed = discord.Embed()
        super().__init__(timeout=360)
        self.clear_items()
        self.add_items()

    @staticmethod
    def shorten_embed(embed: discord.Embed):
        embed = discord.Embed.from_dict(deepcopy(embed.to_dict()))
        while len(embed) > 6000 and embed.fields:
            embed.remove_field(-1)
        if len(embed) > 6000 and embed.description:
            embed.description = embed.description[: (len(embed.description) - len(embed) - 6000)]
        return embed

    @property
    def current_embed(self):
        if self.embed:
            if len(self.embed) < 6000:
                return self.embed
            else:
                return self.shorten_embed(self.embed)
        return self.default_embed()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user == self.author:
            return True

        await interaction.response.send_message("Only the person that used the command can use this, sucks to suck.", ephemeral=True)

    def add_items(self):
        # Row 0
        self.add_item(discord.ui.Button(label="Edit:", style=discord.ButtonStyle.gray, disabled=True, row=0))
        self.add_item(ModalButton(EditEmbedModal, label="Embed", style=discord.ButtonStyle.blurple, row=0))
        self.add_item(ModalButton(EditAuthorModal, label="Author", style=discord.ButtonStyle.blurple, row=0))
        self.add_item(ModalButton(EditFooterModal, label="Footer", style=discord.ButtonStyle.blurple, row=0))

        # Row 1
        self.add_item(discord.ui.Button(label="Fields:", style=discord.ButtonStyle.gray, disabled=True, row=1))
        self.add_field_button = ModalButton(AddFieldModal, emoji="➕", style=discord.ButtonStyle.green, row=1)
        self.add_item(self.add_field_button)

        self.remove_field_button = RemoveFieldButton(self)
        self.add_item(self.remove_field_button)  # Soon
        self.add_item(ModalButton(EditFooterModal, emoji="✏️", style=discord.ButtonStyle.blurple, row=1))  # Soon

        # Row 2
        self.send_button = SendButton()
        self.send_to_button = SendToButton()
        self.add_item(self.send_button)
        self.add_item(self.send_to_button)
        self.add_item(ModalButton(CopyEmbedModal, label="Copy Embed", style=discord.ButtonStyle.green, row=2))

        # Row 3
        self.characters_button = discord.ui.Button(label="0/6,000 Characters", style=discord.ButtonStyle.gray, disabled=True, row=3)
        self.add_item(self.characters_button)  # Soon
        self.fields_button = discord.ui.Button(label="0/25 Fields", style=discord.ButtonStyle.gray, disabled=True, row=3)
        self.add_item(self.fields_button)  # Soon

    async def update_buttons(self):
        embed = self.embed

        if len(embed.fields) > 25:  # If there are more than 25 fields
            if not self.send_button.disabled:  # If the send button is not disabled yet
                self.send_button.disabled = True  # Disable send buttons
                self.send_to_button.disabled = True

        if len(embed.fields) > 24:  # If there are more than 24 fields (means that more can't be added)
            if not self.add_field_button.disabled:  # If the add fields button is not disabled yet
                self.add_field_button.disabled = True  # Disable add fields button

        if not embed.fields or len(embed.fields) < 1:
            if not self.remove_field_button.disabled:
                self.remove_field_button.disabled = True

        if embed.fields:
            print(embed.fields)
            print("embed.fields exist")
            self.remove_field_button.disabled = False

        if len(embed) > 6000:
            if not self.send_button.disabled:
                self.send_button.disabled = True
                self.send_to_button.disabled = True

        self.characters_button.label = f"{len(embed)}/6,000 Characters"
        self.fields_button.label = f"{len(embed.fields)}/25 Fields"

    def default_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="This is an `example` of a __title__ 👋",
            color=discord.Color.random(),
            description=(
                "This is an example of a description. It can be very long, up to 4,000 characters."
                "It can even have new lines and has full __**MARKDOWN SUPPORT**__ including Discord custom emojis <:star:1036761756011339896>"
                "Lastly, you can even add **hyperlinks** in the description, for example `[Google](https://google.com)` would be [Google](https://google.com)"
            ),
        )
        embed.add_field(name="This is an `example` of a __field__ name ⚒️", value="And this is the value of that field. This field is also inlined-")
        embed.add_field(name="Don't want it all on the same line?", value="This field is not inlined. You can have up to 3 fields in a single line.")
        embed.add_field(
            name="Here is another field that is not inlined",
            value="Field's name can be up to 256 characters, and the value can be up to 1024 characters.",
            inline=False,
        )
        embed.set_author(name="This is the author of the embed", url="https://korino.dev", icon_url="http://cdn.korino.dev/u/IgnZiH.png")
        embed.set_image(url="http://cdn.korino.dev/view/wKPa4M.png")
        embed.set_thumbnail(url="http://cdn.korino.dev/view/hmWJUk.png")
        embed.set_footer(text="This is the footer text", icon_url="http://cdn.korino.dev/view/IgnZiH.png")
        return embed


class Modal(discord.ui.Modal):
    def __init__(self, parent_view: EmbedView):
        self.parent_view = parent_view
        self.update_defaults(parent_view.embed)
        super().__init__()

    def update_embed(self):
        return

    def update_defaults(self, embed: discord.Embed):
        return

    async def on_error(self, interaction: Interaction, error: Exception):
        if isinstance(error, Invalid):
            await self.parent_view.update_buttons()
            await interaction.response.edit_message(embed=self.parent_view.current_embed, view=self.parent_view)
            return await interaction.followup.send(str(error), ephemeral=True)

    async def on_submit(self, interaction: Interaction):
        self.update_embed()
        await self.parent_view.update_buttons()
        return await interaction.response.edit_message(embed=self.parent_view.current_embed, view=self.parent_view)


class EditEmbedModal(Modal, title="Edit Embed"):
    _title = discord.ui.TextInput(label="Embed Title", placeholder="Leave any field empty to remove its content", max_length=256, required=False)
    description = discord.ui.TextInput(
        label="Embed Description", placeholder="This can be up to 4,000 characters long", style=discord.TextStyle.long, required=False
    )
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

    def update_embed(self):
        failed = []
        embed = self.parent_view.embed

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

        if failed:
            raise Invalid("\n".join(failed))


class EditAuthorModal(Modal, title="Edit Embed Author"):
    name = discord.ui.TextInput(label="Author Name", placeholder="Leave any field empty to remove its content", max_length=256, required=False)
    url = discord.ui.TextInput(label="Author URL", placeholder="Must be in a HTTP(S) format", required=False)
    icon = discord.ui.TextInput(label="Author Icon URL", placeholder="Must also be in HTTP(S) format", required=False)

    def update_defaults(self, embed: discord.Embed):
        self.name.default = embed.author.name
        self.url.default = embed.author.url
        self.icon.default = embed.author.icon_url

    def update_embed(self):
        failed = []
        embed = self.parent_view.embed

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

        if failed:
            raise Invalid("\n".join(failed))


class EditFooterModal(Modal, title="Edit Embed Footer"):
    text = discord.ui.TextInput(label="Footer Text", placeholder="Leave any field empty to remove its content", max_length=256, required=False)
    icon = discord.ui.TextInput(label="Footer Icon URL", placeholder="Must also be in HTTP(S) format", required=False)

    def update_defaults(self, embed: discord.Embed):
        self.text.default = embed.footer.text
        self.icon.default = embed.footer.icon_url

    def update_embed(self):
        failed = []
        embed = self.parent_view.embed

        if URL_REGEX.fullmatch(self.icon.value):
            if not self.text.value:
                failed.append("Cannot add URL. Text is required to add a footer.")
        elif self.icon.value:
            if not self.text.value:
                failed.append("Cannot add URL. Text is required to add a footer..")
            failed.append("Icon URL was invalid. Must follow the HTTP(S) format.")

        if self.text.value:
            embed.set_footer(text=self.text.value, icon_url=self.icon.value)

        if failed:
            raise Invalid("\n".join(failed))


class AddFieldModal(Modal, title="Add Field"):
    name = discord.ui.TextInput(label="Field Name", max_length=256, required=True)
    value = discord.ui.TextInput(label="Field Value", max_length=1024, required=True)
    inline = discord.ui.TextInput(label="Is Inline?", placeholder="Yes (default) or No", max_length=3, required=False)
    index = discord.ui.TextInput(
        label="Index", placeholder="Where to place the field, a number between 1 and 25. Default is 25 (last)", required=False
    )

    def update_embed(self):
        failed = []

        if self.index.value:
            try:
                index = int(self.index.value) - 1
                return self.parent_view.embed.insert_field_at(
                    index=index, name=self.name.value, value=self.value.value, inline=utils.to_boolean(self.inline.value)
                )

            except Exception as e:
                return self.parent_view.embed.add_field(name=self.name.value, value=self.value.value, inline=utils.to_boolean(self.inline.value))

        self.parent_view.embed.add_field(name=self.name.value, value=self.value.value, inline=utils.to_boolean(self.inline.value))


class RemoveFieldDropdown(discord.ui.Select):
    def __init__(self, parent_view: EmbedView, options: List[discord.SelectOption]):
        self.parent_view = parent_view
        super().__init__(placeholder="Choose the field...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        for value in self.values:
            index = int(value.split(")")[0]) - 1
            self.parent_view.embed.remove_field(index)
            await self.parent_view.update_buttons()
            return await interaction.response.edit_message(embed=self.parent_view.current_embed, view=self.parent_view)


class RemoveFieldView(discord.ui.View):
    def __init__(self, parent_view: EmbedView):
        super().__init__()

        self.options = []
        for i, field in enumerate(parent_view.embed.fields):
            self.options.append(discord.SelectOption(label=f"{i + 1}) {field.name}"))

        self.add_item(RemoveFieldDropdown(parent_view, self.options))


class RemoveFieldButton(discord.ui.Button):
    def __init__(self, parent_view: EmbedView):
        self.parent_view = parent_view
        super().__init__(emoji="➖", style=discord.ButtonStyle.red, disabled=True, row=1)

    async def callback(self, interaction: Interaction):
        return await interaction.response.send_message(embed=self.parent_view.embed, view=RemoveFieldView(self.parent_view))


class CopyEmbedModal(Modal, title="Copy Embed"):
    message = discord.ui.TextInput(
        label="Message Link", placeholder="The link of the message featuring the embed (right click -> copy message link)", required=True
    )

    def update_defaults(self, embed: discord.Embed):
        return

    # We cannot use update_embed here sadly
    async def on_submit(self, interaction: Interaction):
        match = MESSAGE_REGEX.fullmatch(self.message.value)

        if not match:
            return await interaction.response.send_message(
                "Invalid Message Link. Must follow this format: `https://discord.com/channels/guild_id/channel_id/message_id`"
            )

        guild = interaction.client.get_guild(int(match["guild"]))
        if not guild:
            return await interaction.response.send_message("Invalid guild ID.")

        channel = guild.get_channel(int(match["channel"]))
        if not channel or not isinstance(channel, discord.TextChannel):
            return await interaction.response.send_message("Invalid channel ID.")

        message = channel.get_partial_message(int(match["message"]))
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
        assert interaction.message and interaction.message.embeds and self.view
        return await interaction.response.send_modal(self.modal(self.view))


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

    @discord.ui.select(
        cls=discord.ui.ChannelSelect,
        placeholder="Select a channel...",
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
        assert interaction.guild and isinstance(interaction.user, discord.Member) and interaction.message
        channel = interaction.guild.get_channel_or_thread(select.values[0].id)
        assert isinstance(channel, discord.abc.Messageable)

        if not channel.permissions_for(interaction.user).send_messages:
            return await interaction.response.send_message("You can't send messages in that channel.", ephemeral=True)

        embed = interaction.message.embeds[0]
        await interaction.message.delete()

        await channel.send(embed=embed)
        return await interaction.response.send_message(f"Embed was sent to {channel.mention}", ephemeral=True)


class SendToButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Send To", style=discord.ButtonStyle.green, row=2)

    async def callback(self, interaction: Interaction):
        if not interaction.message:
            return await interaction.response.send_message("No message was found. Try again.")

        return await interaction.response.edit_message(embed=interaction.message.embeds[0], view=SendToView())
