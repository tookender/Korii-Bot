import discord
from discord.ext import commands, tasks

from utils import Cog
import logging


class AvatarsCog(Cog):
    def cog_load(self):
        self.update_avatars.start()

    def cog_unload(self):
        self.update_avatars.cancel()

    @tasks.loop(minutes=5)
    async def update_avatars(self):
        rustbyte_guild = self.bot.get_guild(1096226282292920403)

        if not isinstance(rustbyte_guild, discord.Guild):
            logging.error("Cannot find Rustbyte guild")
            return

        developers_role = rustbyte_guild.get_role(1096354583888003102)

        if not isinstance(developers_role, discord.Role):
            logging.error("Cannot find Developers role")
            return

        for member in rustbyte_guild.members:
            if developers_role in member.roles:
                assert member.avatar
                await self.bot.pool.execute(
                    "INSERT INTO avatars(user_id, avatar_url) VALUES ($1, $2) ON CONFLICT(user_id) DO UPDATE SET avatar_url = $2",
                    member.id,
                    member.avatar.replace(size=256, format="webp").url,
                )
