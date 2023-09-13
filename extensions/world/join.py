import contextlib
import random

import discord
from discord.ext import commands

from utils import Embed, Korii


class JoinCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @commands.Cog.listener("on_member_join")
    async def ping_new_member(self, member: discord.Member):
        if member.guild.id != 1059116571215278121:
            return

        channel = self.bot.get_channel(1069276775055638548)

        assert isinstance(channel, discord.TextChannel)

        return await channel.send(member.mention, allowed_mentions=discord.AllowedMentions.all())
