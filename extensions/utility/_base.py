from discord.ext import commands

from bot import Korii


class UtilityBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.description = "😎 | Lots of useful utility commands."
        self.active_games = {}
