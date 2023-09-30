
import asyncio
import logging

import asyncpg
import discord
from aiohttp import ClientSession
from discord import app_commands
from discord.ext import commands

import config
from utils.subclasses.bot import Korii


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