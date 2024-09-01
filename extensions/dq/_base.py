from discord.ext import commands

from bot import Korii

class DQBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.description = "🥷 | Commands for the Dungeon Quest game"