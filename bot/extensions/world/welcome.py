"""
Korii Bot: A multipurpose bot with swag 😎
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

import discord
from discord.ext import commands

from bot import Embed, Interaction

from .reaction_roles import ReactionRoleView


class WelcomeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="📜", label="Rules", style=discord.ButtonStyle.blurple, custom_id="world:rules")
    async def rules(self, interaction: Interaction, button: discord.ui.Button):
        embed = Embed(
            title="📜 Rules of Korino World",
            description="**` 01. `** Be respectful and kind to all members of the server.\n"
            "**` 02. `** No hate speech or discriminatory language of any kind.\n"
            "**` 03. `** Do not spam or flood the chat with messages.\n"
            "**` 04. `** No NSFW or explicit content is allowed.\n"
            "**` 05. `** Do not share personal information without consent.\n"
            "**` 06. `** No bullying, harassment, or threatening behavior.\n"
            "**` 07. `** Follow the instructions of moderators and administrators.\n"
            "**` 08. `** Do not post links to phishing or malicious websites.\n"
            "**` 09. `** Keep conversations appropriate for the designed channels.\n"
            "**` 10. `** No sharing of pirated or copyrighted content.\n"
            "**` 11. `** Do not impersonate other members or use fake accounts.\n"
            "**` 12. `** Any behavior that violates [**Discord's terms of service**](https://discord.com/terms) or [**Discord's community guideline**](https://discord.com/guidelines) will not be tolerated.",
            color=0x10B981,
        )

        return await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(
        label="Reaction Roles",
        emoji="🎭",
        style=discord.ButtonStyle.green,
        custom_id="world:reaction_roles",
    )
    async def reaction_roles(self, interaction: Interaction, button: discord.ui.Button):
        embed = Embed(title="🎭 Reaction Roles", description="", color=0x10B981)

        return await interaction.response.send_message(embed=embed, ephemeral=True, view=ReactionRoleView())


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def welcome(self, ctx: commands.Context):
        if not ctx.message.reference:
            return await ctx.send("No reply.")

        message = ctx.message.reference.resolved

        if not isinstance(message, discord.Message):
            return await ctx.send("Invalid reply.")

        embed = Embed(
            title="👋 Welcome to Korino World!",
            description="Korino World is a chill and welcoming community server."
            "We offer a lot of stuff including giveaways, events, a Minecraft Server and more!\n\n"
            "Here are the top things to do:\n"
            "**` - `** 📖 Read the rules by clicking **📜 Rules**.\n"
            "**` - `** 🎭 Grab some personal roles by clicking **🎭 Personal Roles**\n"
            "**` - `** 🛠️ Learn more about our projects and us by visiting [**our website**](https://spooki.xyz).\n"
            "**` - `** 💬 Chat with other people and make friends in <#1063817144128766033>.",
            color=0x10B981,
        )

        return await message.edit(content=None, embed=embed, view=WelcomeView())
