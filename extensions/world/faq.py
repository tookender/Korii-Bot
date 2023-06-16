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
from discord.ext.commands import command
from discord.ui import button

from bot import Korii
from utils import Embed, Interaction


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

    async def on_submit(self, interaction: Interaction):
        return

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        return


class FAQView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(
            emoji="💻",
            label="Modifications",
            style=discord.ButtonStyle.blurple,
            custom_id="world:modifications"
    )
    async def modifications(self, interaction: Interaction, button: discord.ui.Button):
        addons = """
            **Anti Combat Log:** Prevent people from logging while in combat.
            **Auction House:** Using the auction house you can sell or buy items using our in-game currency. /ah
            **Concrete Mixer:** Put concrete powder into a cauldron to get concrete.
            **Levelled Mobs:** All mobs spawn with a different level. Higher level = higher damage, drops, etc.
            **Auto Pickup:** Automatically pick up items.
            **Skills:** Skills to earn stat buffs, unlock and level up abilities, and more. /skills

            **Villager Death Messages:** Be notified about when a villager dies.
            **Custom Nether Portals:** Make nether portals no matter the shape and size.
            **No Enderman Grief:** Endermen can no longer pick up blocks.
            **Mltiplayer Sleep:** Only one person has to sleep to skip the night.
            **Armored Elytras:** Drop a chestplate and an elytra on an anvil to combine the two.
            **Durability Ping:** Get notified when an item reaches low durability.
            **Fast Leaf Decay:** Leaves decay faster.
            **More Mob Heads:** A small chance to get a mob head from all mobs.
            **Mine Treasure:** Get random treasure chests from mining depending on the biome.
            **Timber:** Break trees, faster.
            **Graves:** If you die, a grave will spawn, right click it to get all your items back.
        """

        modifications = [
            "Villagers follow emerald blocks.",
            "You can silk touch spawners.",
            "Bows with infinity + mending.",
            "Right click to edit signs.",
            "Ender chests have 6 rows.",
            "Use colors in signs.",
            "Better mending.",
            "Flying squids.",
        ]

        embed = Embed(
            title="List of modifications",
            description=addons,
        )

        embed.add_field(
            name="Modifications",
            value="\n".join([f"- {modification}" for modification in modifications]),
            inline=False,
        )

        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )

    @button(
        emoji="⚡",
        label="Levelling Rewards",
        style=discord.ButtonStyle.blurple,
        custom_id="world:levelling_rewards",
    )
    async def levelling_rewards(self, interaction: Interaction, button: discord.ui.Button):
        rewards = [
            "<@&1069284713056977006> Custom color roles",
            "<@&1069284714311057478> Host your own events",
            "<@&1069284715498053632> More color roles, higher chance of Simon",
            "<@&1069284717821710368> Create private threads, color roles",
            "<@&1069284719197442129> Start activities, use stickers",
            "<@&1069284720086634637> Send links, stream, create public threads",
            "<@&1069284769000587336> Change your nickname, add reactions",
        ]

        embed = Embed(
            title="⚡ Levelling Rewards",
            description="\n".join([f"**` - `** {reward}" for reward in rewards]),
        )

        return await interaction.response.send_message(embed=embed, ephemeral=True)

    @button(emoji="🎫", label="Create Ticket", style=discord.ButtonStyle.green, custom_id="world:ticket")
    async def create_ticket(self, interaction: Interaction, button: discord.ui.Button):
        return await interaction.response.send_message(
            "This feature is coming soon, for the time being, you can contact the server owner.",
            ephemeral=True,
        )
        # return await interaction.response.send_modal(TicketModal())


class FAQCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @command()
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
            color=0x10B981,
        )

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
            value="[Click here](https://bot.korino.dev) to invite it.",
            inline=False,
        )

        embed.add_field(
            name="4️⃣ How do I join the Korino PvP Minecraft Server?",
            value="[Click here](https://korino.dev/pvp) to visit the Korino PvP website.",
            inline=False,
            title=False,
        )

        embed.add_field(
            name="5️⃣ What modifications are on the Korino SMP?",
            value="Click the **💻 Modifications** button below to view them.",
            inline=False,
            title=False,
        )

        embed.add_field(
            name="6️⃣ Are there any levelling rewards?",
            value="Yes, for more info click the **⚡ Levelling Rewards** button below.",
            inline=False,
        )

        embed.add_field(
            name="7️⃣ Why are some buttons blue and some green?",
            value="Blue buttons not interactive and send text/info. Green buttons are interactive buttons which you can interact with after pressing.",
            inline=False,
        )

        embed.add_field(
            name="8️⃣ My question was not answered here/I need help.",
            value="Create a ticket by clicking the **🎫 Create Ticket** button below.",
            inline=False,
        )

        return await message.edit(content=None, embed=embed, view=FAQView())
