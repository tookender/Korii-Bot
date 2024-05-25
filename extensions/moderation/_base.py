from discord.ext import commands

from bot import Korii


class ModerationBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.description = "💥 | Moderation to get rid of dog haters."
