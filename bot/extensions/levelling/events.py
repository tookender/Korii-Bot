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

import math
import random
from typing import Optional

import discord
from discord.ext import commands

from bot import Embed, Korii, LevellingCacheManager


class EventsCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.cooldown: commands.CooldownMapping = commands.CooldownMapping.from_cooldown(1, 45, commands.BucketType.member)

    @property
    def cache(self) -> LevellingCacheManager:
        return self.bot.levelling_cache

    # What we the on_message to do: (rewrite)
    # 1. Cooldown checks
    # 2. Check if message.guild has levelling enabled
    # 3. Give random amount of XP between 24 and 32, from 4 and 7 more if the message content is more than 30
    # 4. Update the XP
    # 5. If they levelled up: Send a level up message
    # 6. If they levelled up: Give them roles if there are any role rewards in the guild for that level

    @commands.Cog.listener("on_message")
    async def levelling(self, message: discord.Message):
        if not message.guild or message.author.bot or isinstance(message.author, discord.User):
            # If the message isn't sent in a guild, or the message author is a bot or the member is an instance of a discord.User, we return
            return

        guild_levelling = await self.bot.pool.fetchval("SELECT levelling_enabled FROM guilds WHERE guild_id = $1", message.guild.id)
        if not guild_levelling:
            # If the guild doesn't have levelling enabled we return
            return

        bucket = self.cooldown.get_bucket(message)
        if bucket:
            retry_after = bucket.update_rate_limit()
        else:
            retry_after = None

        if retry_after:
            # If the user still has a message cooldown we return
            return

        # Amount of XP the user should get for the message
        random_xp = random.randint(24, 34) + (random.randint(4, 7) if len(message.content) > random.randint(34, 44) else 0)
        data = await self.bot.pool.fetchrow(
            "SELECT level, xp FROM levels WHERE guild_id = $1 AND user_id = $2",
            message.guild.id,
            message.author.id,
        )

        if not data:
            # If the user doesn't have any data in the database we add them into the database
            return await self.bot.pool.execute(
                "INSERT INTO levels (guild_id, user_id, level, xp) VALUES ($1, $2, $3, $4)",
                message.guild.id,
                message.author.id,
                0,
                random_xp,
            )

        # This is the amount of required XP for the next level, each level is 300 XP more than the previous
        required_xp = math.floor(10 * (data[0] ^ 2) + (55 * data[0]) + 100)

        if (data[1] + random_xp) > required_xp:
            await self.bot.pool.execute(
                "UPDATE levels SET level = $1, xp = $2 WHERE guild_id = $3 AND user_id = $4",
                data[0] + 1,
                0,
                message.guild.id,
                message.author.id,
            )
            role = await self.bot.pool.fetchval(
                "SELECT role_id FROM role_rewards WHERE guild_id = $1 AND level = $2",
                message.guild.id,
                data[0] + 1,
            )
            description = ""

            if role:
                role = message.guild.get_role(role)

                if role:
                    try:
                        await message.author.add_roles(role)
                        description = f"You have received the {role.mention} role."

                    except Exception as error:
                        description = f"I couldn't give you the {role.mention} role.```prolog\n{error}\n```"

            embed = Embed(title=f"⚡ Level {data[0]} → Level {data[0] + 1}", description=description)
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar)

            return await message.reply(embed=embed)

        return await self.bot.pool.execute(
            "UPDATE levels SET xp = $1 WHERE guild_id = $2 AND user_id = $3",
            data[1] + random_xp,
            message.guild.id,
            message.author.id,
        )
