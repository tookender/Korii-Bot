import discord
from discord.ext import commands

from ._base import EventsBase


class GhostCog(EventsBase):
    @commands.Cog.listener("on_message")
    async def ghost(self, message: discord.Message):
        if message.author.bot:
            return

        if message.content.lower() == "<:ghoost:1228090615510732850>":
            return await message.reply("G-HOOOOOOST <:ghoost:1228090615510732850>", silent=True)

        if message.content.lower() == "👻":
            return await message.reply("G-HOOOOOOST 👻", silent=True)
