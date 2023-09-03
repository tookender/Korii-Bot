import contextlib
import random

import discord
from discord.ext import commands, tasks

from utils import Embed, Korii
import logging


class AvatarsCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.update_avatars.start()
        self.rustbyte_guild: discord.Guild
        self.developers_role: discord.Role

    def cog_unload(self):
        self.update_avatars.cancel()

    @tasks.loop(minutes=5)
    async def update_avatars(self):
        for member in self.rustbyte_guild.members:
            if self.developers_role in member.roles:
                assert member.avatar
                await self.bot.pool.execute("INSERT INTO avatars(user_id, avatar_url) VALUES ($1, $2) ON CONFLICT(user_id) DO UPDATE SET avatar_url = $2",
                                            member.id, member.avatar.replace(size=256, format="webp"))

    @update_avatars.before_loop
    async def wait_until_ready(self):
        await self.bot.wait_until_ready()

        guild = self.bot.get_guild(1096226282292920403)
        if not isinstance(guild, discord.Guild):
            logging.error("Cannot find Rustbyte guild")
            return
        
        self.rustbyte_guild = guild

        role = guild.get_role(1096354583888003102)
        if not isinstance(role, discord.Role):
            logging.error("Cannot find Developers role in Rustbyte guild")
            return
        
        self.developers_role = role