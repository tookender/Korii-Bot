import typing
import random
import discord

from discord import Interaction
from discord.ext import commands
from typing import TYPE_CHECKING

from utils import tick
from discord import PartialEmoji, ButtonStyle, Interaction

if TYPE_CHECKING:
    from bot import Korii
else:
    from discord.ext.commands import Bot as Korii

target_type = typing.Union[discord.Member, discord.User, discord.PartialEmoji, discord.Guild, discord.Invite]

class ConfirmButton(discord.ui.Button):
    def __init__(self, label: str, emoji: str, button_style: discord.ButtonStyle):
        super().__init__(style=button_style, label=label, emoji=emoji, )

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Confirm = self.view
        view.value = True
        view.stop()


class CancelButton(discord.ui.Button):
    def __init__(self, label: str, emoji: str, button_style: discord.ButtonStyle):
        super().__init__(style=button_style, label=label, emoji=emoji)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Confirm = self.view
        view.value = False
        view.stop()


class Confirm(discord.ui.View):
    def __init__(self, buttons: typing.Tuple[typing.Tuple[typing.Optional[typing.Union[PartialEmoji, str]], str, ButtonStyle], typing.Tuple[typing.Optional[typing.Union[PartialEmoji, str]], str, ButtonStyle]], timeout: int = 30):
        super().__init__(timeout=timeout)
        self.message = None
        self.value = None
        self.ctx: CustomContext = None
        self.add_item(ConfirmButton(emoji=buttons[0][0],
                                    label=buttons[0][1],
                                    button_style=(
                                            buttons[0][2] or discord.ButtonStyle.green
                                    )))
        self.add_item(CancelButton(emoji=buttons[1][0],
                                   label=buttons[1][1],
                                   button_style=(
                                           buttons[1][2] or discord.ButtonStyle.red
                                   )))

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user and interaction.user.id in (self.ctx.bot.owner_id, self.ctx.author.id):
            return True
        messages = [
            "Oh no you can't do that! This belongs to **{user}**",
            'This is **{user}**\'s confirmation, sorry! 💢',
            '😒 Does this look yours? **No**. This is **{user}**\'s confirmation button',
            f'STOP IT GET SOME HELP',
            'HEYYYY!!!!! this is **{user}**\'s menu.',
            'Sorry but you can\'t mess with **{user}**\' menu :(',
            'No. just no. This is **{user}**\'s menu.',
            'Stop.',
            'You don\'t look like {user} do you...',
            '🤨 That\'s not yours! That\'s **{user}**\'s menu',
            '🧐 Whomst! you\'re not **{user}**',
            '_out!_ 👋'
        ]
        await interaction.response.send_message(random.choice(messages).format(user=self.ctx.author.display_name),
                                                ephemeral=True)

        return False


class CustomContext(commands.Context):
    bot: Korii

    @staticmethod
    def default_tick(opt: bool, text: str = None) -> str:
        emoji = tick(opt)
        if text:
            return f"{emoji} {text}"
        return emoji

    async def confirm(self, message: str = 'Do you want to confirm?',
                      buttons: typing.Optional[typing.Tuple[typing.Union[discord.PartialEmoji, str],
                                            str, discord.ButtonStyle]] = None, timeout: int = 30,
                      delete_after_confirm: bool = False,
                      delete_after_timeout: bool = False,
                      delete_after_cancel: bool | None = None,
                      return_message: bool = False) \
            -> typing.Union[bool, typing.Tuple[bool, discord.Message]]:
        """ A confirmation menu. """

        delete_after_cancel = delete_after_cancel if delete_after_cancel is not None else delete_after_confirm

        view = Confirm(buttons=buttons or (
            (None, 'Confirm', discord.ButtonStyle.green),
            (None, 'Cancel', discord.ButtonStyle.red)
        ), timeout=timeout)
        view.ctx = self
        message = await self.send(message, view=view)
        await view.wait()
        if False in (delete_after_cancel, delete_after_confirm, delete_after_timeout):
            view.children = [view.children[0]]
            for c in view.children:
                c.disabled = True
                if view.value is False:
                    c.label = 'Cancelled!'
                    c.emoji = None
                    c.style = discord.ButtonStyle.red
                elif view.value is True:
                    c.label = 'Confirmed!'
                    c.emoji = None
                    c.style = discord.ButtonStyle.green
                else:
                    c.label = 'Timed out!'
                    c.emoji = '⏰'
                    c.style = discord.ButtonStyle.gray
        view.stop()
        if view.value is None:

            try:
                if return_message is False:
                    (await message.edit(view=view)) if delete_after_timeout is False else (await message.delete())
            except (discord.Forbidden, discord.HTTPException):
                pass
            return (None, message) if delete_after_timeout is False and return_message is True else None

        elif view.value:

            try:
                if return_message is False:
                    (await message.edit(view=view)) if delete_after_confirm is False else (await message.delete())
            except (discord.Forbidden, discord.HTTPException):
                pass
            return (True, message) if delete_after_confirm is False and return_message is True else True

        else:

            try:
                if return_message is False:
                    (await message.edit(view=view)) if delete_after_cancel is False else (await message.delete())
            except (discord.Forbidden, discord.HTTPException):
                pass

            return (False, message) if delete_after_cancel is False and return_message is True else False