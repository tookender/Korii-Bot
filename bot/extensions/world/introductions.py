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

from bot import Embed, Korii, Interaction


class IntroductionsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Template", emoji="📋", custom_id="world:view_example", style=discord.ButtonStyle.blurple)
    async def template(self, interaction: Interaction, button: discord.ui.Button):
        template = [
            "👋 Hello my name is **[name]**",
            "⏰ I am **[age]** years old.",
            "🌎 I am from **[country]**.",
            "🎮 My hobbies are **[hobbies]**.",
        ]
        
        embed = Embed(
            title="🎭 Template",
            description="\n".join(template),
        )

        embed.set_footer(text="You can modify this template as much as you like. You also don't have to use it, and you can just make your own.")

        return await interaction.response.send_message(embed=embed, ephemeral=True)

class IntroductionsCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def introductions(self, ctx: commands.Context):
        if not ctx.message.reference:
            return await ctx.send("No reply.")
        
        message = ctx.message.reference.resolved

        if not isinstance(message, discord.Message):
            return await ctx.send("Invalid reply.")

        embed = Embed(
            title="🎭 Introductions",
            description="Here you can introduce yourself to the rest of the server.\n"
                        "Click the button below for a template you can use, you can also make your own if you wanna get creative.",
            color=0x10b981,
        )
        
        return await message.edit(content=None, embed=embed, view=IntroductionsView())