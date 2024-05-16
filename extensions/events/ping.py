import random

import discord
from discord.ext import commands

from ._base import EventsBase


class PingCog(EventsBase):
    @commands.Cog.listener("on_message")
    async def ping(self, message: discord.Message):
        if message.reference and message.reference.resolved:
            return

        bucket = self.bot.ping_cooldown.get_bucket(message)

        if bucket:
            retry_after = bucket.update_rate_limit()
        else:
            retry_after = None

        if retry_after:
            return

        if str(self.bot.user.id) in message.content.lower():
            return await message.reply(random.choice(self.bot.messages))
