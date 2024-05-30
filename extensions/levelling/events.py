import math
import random

import discord
from discord.ext import commands

from utils import Cog, Embed

from ._base import LevellingBase


class EventsCog(LevellingBase):
    @commands.Cog.listener("on_message")
    async def levelling(self, message: discord.Message):
        if not message.guild or message.author.bot or isinstance(message.author, discord.User):
            # If the message isn't sent in a guild, or the message author is a bot or the member is an instance of a discord.User, we return
            return

        guild_levelling = await self.bot.pool.fetchval("SELECT levelling_enabled FROM guilds WHERE guild_id = $1", message.guild.id)
        if not guild_levelling:
            # If the guild doesn't have levelling enabled we return
            return

        bucket = self.bot.levelling_cooldown.get_bucket(message)
        if bucket:
            retry_after = bucket.update_rate_limit()
        else:
            retry_after = None

        if retry_after:
            # If the user still has a message cooldown we return
            pass

        # Amount of XP the user should get for the message
        random_xp = random.randint(24, 34) + (random.randint(4, 7) if len(message.content) > random.randint(34, 44) else 0)

        multiplier = await self.bot.pool.fetchval("SELECT levelling_multiplier FROM guilds WHERE guild_id = $1", message.guild.id)
        random_xp = random_xp * multiplier

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

            embed = Embed(title=f"⚡ Level {data[0]} → Level {data[0] + 1}", description=f"\n\n{description}")
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar)

            message_formats = {
                "user": message.author.display_name,
                "user_mention": message.author.mention,
                "guild": message.guild.name,
                "level": data[0] + 1,
            }
            message_format = await self.bot.pool.fetchval("SELECT levelling_message FROM guilds WHERE guild_id = $1", message.guild.id)
            channel_id = await self.bot.pool.fetchval("SELECT levelling_channel FROM guilds WHERE guild_id = $1", message.guild.id)

            if not channel_id:
                channel = message.channel
            else:
                channel = message.guild.get_channel(channel_id)

            if channel == message.channel:
                return await message.reply(content=message_format.format(**message_formats), embed=embed)

            if not isinstance(channel, discord.TextChannel):
                return

            return await channel.send(content=message_format.format(**message_formats), embed=embed)

        return await self.bot.pool.execute(
            "UPDATE levels SET xp = $1 WHERE guild_id = $2 AND user_id = $3",
            data[1] + random_xp,
            message.guild.id,
            message.author.id,
        )
