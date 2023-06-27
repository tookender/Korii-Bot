"""
Korii Bot: A multi-purpose bot with swag 😎
Copyright (C) 2023 Ender2K89

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import contextlib
import random

import discord
from discord.ext import commands

from utils import Embed, Korii


class PingCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.cooldown: commands.CooldownMapping = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.guild)

    @commands.Cog.listener("on_message")
    async def ping(self, message: discord.Message):
        if message.reference and message.reference.resolved:
            return

        bucket = self.cooldown.get_bucket(message)
        
        if bucket:
            retry_after = bucket.update_rate_limit()
        else:
            retry_after = None

        if retry_after:
            return
        
        if str(self.bot.user.id) in message.content.lower():
            return await message.reply("fuck off")
