from discord.ext import commands

from bot import Korii


class FunBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.description = "🎈 | Plenty of fun commands to just mess around with."
