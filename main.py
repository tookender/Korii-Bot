import discord
import asyncio
from bot import Korii
from discord import app_commands

bot: Korii = Korii(intents=discord.Intents.all())

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
    bot.tree.on_error = on_error
    await bot.start()

if __name__ == "__main__":
    asyncio.run(run_bot())
