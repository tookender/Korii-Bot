import random

import discord
from discord.ext import commands

from bot import Korii
from utils import Embed, Interaction
from utils.commands import *
from utils.constants import NOT_YOUR_BUTTON
from utils.context import CustomContext

from ._base import HelpBase


class CategoryDropdown(discord.ui.Select):
    def __init__(self, options: list[discord.SelectOption]):
        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options, row=1)

    async def callback(self, interaction: discord.Interaction):
        embed = Embed()
        await interaction.response.send_message(f"**You chose:** `{self.values[0]}`")


class HelpView(discord.ui.View):
    message: discord.Message

    def __init__(self, author: discord.Member | discord.User, categories: list[discord.SelectOption]):
        super().__init__(timeout=300)

        self.author = author
        self.add_item(CategoryDropdown(categories))

    async def interaction_check(self, interaction: Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(f"{random.choice(NOT_YOUR_BUTTON).replace('[user]', self.author.display_name)}", ephemeral=True)
            return False

        return True

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button) or isinstance(child, discord.ui.Select):
                child.disabled = True

        await self.message.edit(view=self)

    @discord.ui.button(label="Help", emoji="❓", style=discord.ButtonStyle.green, row=2)
    async def help(self, interaction: Interaction, _):
        embed = Embed(
            title="Help Menu: Guide",
            description=f"`<argument>`\n"
            f"This means that the argument is **REQUIRED**.\n\n"
            f"`[argument]`\n"
            f"This means that the argument is **OPTIONAL**.\n\n"
            f'`[argument="default"]`\n'
            f"This means that the argument is **OPTIONAL** and has a default value, which you can see inside of the quotation marks.\n\n"
            f"An argument is basically what comes after a command. For example:\n"
            f'`s!balance [user="you"]`\n'
            f"In this example, the argument is an OPTIONAL user, aka the user you are viewing the balance of.\n"
            f"It also has a default value, which defaults to **you**, aka the one using the command.\n\n"
            f"⚠️ **DO NOT** use these brackets (`[]`, `<>`) when running a command.\n"
            f"They are only there, to indicate whether the argument is required or not.",
        )

        return await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpCog(HelpBase):
    async def send_main_message(self, ctx: CustomContext):
        cogs: list[commands.Cog] = []
        ignored_cogs = ["Events", "Jishaku", "IPC", "Help", "Utility"]

        for cog in self.bot.cogs:
            if cog not in ignored_cogs:
                cog = self.bot.get_cog(cog)
                assert cog
                cogs.append(cog)

        view = HelpView(
            author=ctx.author,
            categories=[
                discord.SelectOption(
                    label=cog.qualified_name, description=cog.description.split(" | ")[1] or "N/A", emoji=cog.description.split(" | ")[0] or None
                )
                for cog in cogs
            ],
        )

        embed = Embed(title="Help Menu", description="👋 Hello there! I'm **Korii Bot**. Welcome to the help menu.")

        embed.add_field(
            name="**Getting help**",
            value=f"To navigate all categories, you can use the dropdown below.\n"
            f"Selecting a category shows you all commands that category has.\n"
            f"Use **{await self.get_prefix(ctx)}help <command>** for more information on a specific command.",
            inline=False,
            title=False,
        )

        embed.add_field(
            name="**Who are you?**",
            value=f"I'm a multi-purpose Discord bot created by [**@tookender**](https://korino.dev).\n"
            f"You can use my commands to moderate your server, get cute dog images, or even gamble!",
            inline=False,
            title=False,
        )

        embed.set_footer(text="Buttons expire after 5 minutes of no use.")

        try:
            message = await ctx.send(embed=embed, view=view)
        except discord.HTTPException:
            return
        else:
            if view is not discord.utils.MISSING:
                view.message = message

    async def send_command_message(self, ctx: CustomContext, command: commands.Command) -> discord.Message:
        signature = command.signature

        arguments = get_arguments(command)
        formatted_arguments = []
        for name, description in arguments.items():
            formatted_arguments.append(f"**{name}:** {description}")

        nl = "\n"

        embed = Embed(
            description=f"{format_command(command)}\n" f"{command.description}\n\n" f"__**Arguments**__\n" f"{nl.join(formatted_arguments)}\n",
        )

        return await ctx.send(embed=embed)

    @commands.hybrid_command(description="View all categories and commands of the bot.")
    async def help(self, ctx, command: str | None = None):
        if not command:
            return await self.send_main_message(ctx)

        bot_command = self.bot.get_command(command)

        if not bot_command:
            embed = Embed(
                description=f"{self.bot.E['no']} | That command does not exist.",
                colour=discord.Colour.red(),
            )

            embed.set_author(
                name=ctx.author.global_name,
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
            )

            return await ctx.send(embed=embed)

        return await self.send_command_message(ctx, bot_command)
