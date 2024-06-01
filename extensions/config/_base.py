from discord.ext import commands

from bot import Korii


class ConfigBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.description = "🔎 | For setting up Korii in your server."

    group: commands.HybridGroup = commands.hybrid_group(name="config", description="Configure your guild's bot configuration.")
