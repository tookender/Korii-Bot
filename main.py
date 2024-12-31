import asyncio

import discord
from discord import app_commands
import discord.gateway

from bot import Korii
import ast
import inspect
import re

# s: https://medium.com/@chipiga86/python-monkey-patching-like-a-boss-87d7ddb8098e
def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)


source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(
    r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',  # hh this regex
    r"\1Discord Android\2",  # s: https://luna.gitlab.io/discord-unofficial-docs/mobile_indicator.html
    source_
)

loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]

bot: Korii = Korii()


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
