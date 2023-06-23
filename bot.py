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

import asyncio
import logging

import asyncpg
import discord
from aiohttp import ClientSession
from discord import app_commands

import config
from utils.subclasses.bot import Korii


discord.VoiceClient.warn_nacl = False


async def interaction_check(interaction: discord.Interaction[Korii]):
    if interaction.client.maintenace:
        return False
    return True

async def on_error(interaction: discord.Interaction[Korii], error: app_commands.AppCommandError):
    embed = discord.Embed(
        title=f"{interaction.client.E['warning']} Error",
        color=discord.Color.red(),
    )

    embed.add_field(name="Reason", value=error)

    if interaction.response.is_done():
        return await interaction.followup.send(embed=embed, ephemeral=True)

    return await interaction.response.send_message(embed=embed, ephemeral=True)


async def run_bot() -> None:
    discord.utils.setup_logging(level=logging.INFO)

    async with ClientSession() as session, asyncpg.create_pool(config.DATABASE) as pool,\
        Korii(session=session, pool=pool) as bot:

        bot.tree.interaction_check = interaction_check
        bot.tree.on_error = on_error

        try:
            await bot.start(config.BOT_TOKEN)
        
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    asyncio.run(run_bot())