import random

import discord
from discord.ext import commands

from bot import Embed, Korii


class EventsCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 45, commands.BucketType.member)

    async def give_roles(self, guild: discord.Guild, user: discord.Member):
        ...
    
    @commands.Cog.listener("on_message")
    async def levelling(self, message: discord.Message):
        if not message.author.id == 1022842005920940063:
            return

        if not message.guild or message.author.bot or isinstance(message.author, discord.User):
            # If the message isn't sent in a guild, or the message author is a bot or the member is an instance of a discord.User, we return
            return
        
        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            # If the user still has a message cooldown we return
            return
        
        guild_levelling = await self.bot.pool.fetchval("SELECT levelling_enabled FROM guilds WHERE guild_id = $1", message.guild.id)

        if not guild_levelling:
            # If the guild doesn't have levelling enabled we return
            return
        
        # Amount of XP the user should get for the message
        random_xp = random.randint(21, 33) + (random.randint(4, 7) if len(message.content) > random.randint(31, 46) else 0)
        data = await self.bot.pool.fetchrow("SELECT level, xp FROM levels WHERE guild_id = $1 AND user_id = $2")

        if not data:
            # If the user doesn't have any data in the database we add them into the database
            return await self.bot.pool.execute("INSERT INTO levels (guild_id, user_id, level, xp) VALUES ($1, $2, $3, $4)", message.guild.id, message.author.id, 0, random_xp)

        # This is the amount of required XP for the next level, each level is 300 XP more than the previous
        required_xp = 300 * (data[0] + 1)

        if (data[1] + random_xp) > required_xp:
            await self.bot.pool.execute("UPDATE levels SET level = $1, xp = $2 WHERE guild_id = $3 AND user_id = $4", data[0] + 1, 0, message.guild.id, message.author.id,)
            
            embed = Embed()
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar)
            