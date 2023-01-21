import contextlib
import random

import discord
from bot import Korii
from discord.ext import commands
from utilities.classes.embed import Embed


class GuildCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @commands.Cog.listener("on_guild_join")
    async def smash_or_pass(self, guild: discord.Guild):
        assert guild.owner

        if len([member for member in guild.members if member.bot]) > 20:
            embed = Embed(
                title=f"💔 Too many robots",
                description="Your server has more than 20 robots in it, which means it could be a bot farm.\n"
                "So sadly I will have to leave your server until you have less than 20 robots in your server.",
            )

            try:
                await guild.owner.send(embed=embed)

            except:
                with contextlib.suppress(discord.HTTPException, discord.Forbidden):
                    channel = random.choice(guild.text_channels)
                    await channel.send(embed=embed)

            return await guild.leave()

        embed = Embed(
            title=f"💖 Thanks for choosing Korii",
            description="Thank you for choosing **Korii**. We promise to not let you down.\n"
            "For more information, use the `/help` command.",
        )

        try:
            await guild.owner.send(embed=embed)

        except:
            with contextlib.suppress(discord.HTTPException, discord.Forbidden):
                channel = random.choice(guild.text_channels)
                await channel.send(embed=embed)
