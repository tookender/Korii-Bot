from discord.ext import commands

from bot import Korii


class ConfigBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot