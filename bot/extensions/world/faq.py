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


class TicketModal(discord.ui.Modal, title="🎫 Create Ticket"):
    def __init__(self):
        super().__init__(timeout=360)
    
    code = discord.ui.TextInput(
        label="Code",
        placeholder="The code here...",
        min_length=4,
        max_length=4,
        required=True,
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        return


    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        return


class FAQView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="⚡", label="Levelling Rewards", style=discord.ButtonStyle.blurple, custom_id="world:levelling_rewards")
    async def levelling_rewards(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = Embed(
            title="⚡ Levelling Rewards",
            description="",
        )

        # server booster - 
        # legend - custom color role
        # master - host your own events/giveaways
        # professional - more color roles, higher chance of simon in simon says
        # experienced - create private threads, color roles
        # apprentice - start activites, use stickers
        # intermediate - send links, stream, create public threads
        # beginner - change nickname, add reactions

        return await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji="🎫", label="Create Ticket", style=discord.ButtonStyle.green, custom_id="world:verify")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        return await interaction.response.send_message("This feature is coming soon, for the time being, you can contact the server owner.")
        #return await interaction.response.send_modal(TicketModal())


class FAQCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def faq(self, ctx: commands.Context):
        if not ctx.message.reference:
            return await ctx.send("No reply.")
        
        message = ctx.message.reference.resolved

        if not isinstance(message, discord.Message):
            return await ctx.send("Invalid reply.")

        embed = Embed(
            title="❓ Frequently Asked Questions",
            description="Here are some frequently asked questions.",
            color=0x10b981)
        
        embed.add_field(
            name="1️⃣ Where are the rules?",
            value="You can find the rules at <#1069276775055638548> by clicking the **📜 Rules** button.",
            inline=False,
        )

        embed.add_field(
            name="2️⃣ How do I get reaction roles?",
            value="You can get reaction roles at <#1069276775055638548> by clicking the **🎭 Reaction Roles** button.",
            inline=False,        
        )

        embed.add_field(
            name="3️⃣ Where can I invite Korii?",
            value="[Click here](https://bot.spooki.xyz) to invite it.",
            inline=False,
        )

        embed.add_field(
            name="4️⃣ How do I join the Korino PvP Minecraft Server?",
            value="[Click here](https://spooki.xyz/pvp) to visit the Korino PvP website.",
            inline=False,
        )

        embed.add_field(
            name="5️⃣ My question was not answered here/I need help.",
            value="Create a ticket by clicking the **🎫 Create Ticket** button below.",
            inline=False,
        )

        embed.add_field(
            name="6️⃣ Are there any levelling rewards?",
            value="Yes, for more info click the **⚡ Levelling Rewards** button below.",
            inline=False,
        )
        
        return await message.edit(content=None, embed=embed, view=FAQView())