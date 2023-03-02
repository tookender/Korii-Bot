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

from bot import Embed, Korii


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
            description="Here you can introduce yourself to the rest of the server.",
            color=0x10b981,
        )
        
        return await message.edit(content=None, embed=embed, view=IntroductionsView())