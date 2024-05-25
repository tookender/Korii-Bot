from discord.ext import commands

from bot import Korii


class LevellingBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.description = "⚡ | Levelling module with commands to view your level."
