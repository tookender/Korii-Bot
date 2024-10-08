from typing import Optional, Union

import discord
from discord import Colour
from discord.ext import commands
from discord.ext.commands import Context

from bot import Korii
from utils import Embed, Interaction

from .utils import *


class GuildContext(commands.Context):
    @property
    def guild(self) -> discord.Guild:
        if not self.guild:
            raise commands.NoPrivateMessage("This command cannot be used outside of a guild.")
        return self.guild


class EconomyBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.description = "💸 | Cool economy system with lots of gambling."

    async def get_prefix(self, ctx):
        if isinstance(ctx, commands.Context):
            prefix = "s!"
        else:
            prefix = "/"

        return prefix

    async def send_embed(
        self,
        ctx,
        text: str,
        color: Optional[Union[Colour, int]] = 0x10B981,
        footer: Optional[str] = None,
        return_embed: Optional[bool] = False,
        author: Optional[discord.Member] = None,
        view: Optional[discord.ui.View] = None,
    ):
        author = author or ctx.author

        embed = Embed(
            description=text,
            colour=color,
        )

        embed.set_author(
            name=author.global_name,
            icon_url=author.avatar.url if author.avatar else None,
        )

        embed.set_footer(text=footer)

        if not return_embed:
            return await ctx.send(embed=embed, silent=True, view=view)
        
        return embed

    async def check_account(self, ctx, user: discord.Member):
        if not await has_account(self.bot, user.id, ctx.guild.id):
            embed = Embed(
                title="❌ No account found",
                description=f"{user.mention} needs to use `/register` to register an account for this guild.",
            )

            await ctx.send(embed=embed, silent=True)
            return True
        else:
            return False

    async def cog_check(self, ctx: Context):
        assert ctx.command and ctx.guild

        if ctx.command.name == "register":
            return True

        if await has_account(self.bot, ctx.author.id, ctx.guild.id):
            return True

        embed = Embed(title="❌ | No account found", description="Please use `s!register` to register an account for this guild in order to use this command.")

        await ctx.send(embed=embed, silent=True)
        return False

    async def interaction_check(self, interaction: Interaction):
        assert interaction.command and interaction.guild

        if interaction.command.name == "register":
            return True

        if await has_account(self.bot, interaction.user.id, interaction.guild.id):
            return True

        embed = Embed(title="❌ | No account found", description="Please use `/register` to register an account for this guild in order to use this command.")

        await interaction.response.send_message(embed=embed, silent=True)
        return False
