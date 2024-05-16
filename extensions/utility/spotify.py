from io import BytesIO

import discord
from discord.ext import commands

import config

from ._base import UtilityBase


class SpotifyCog(UtilityBase):
    @commands.hybrid_command()
    async def spotify(self, ctx: commands.Context, member: discord.Member = commands.Author):
        await ctx.typing()

        spotify: discord.Spotify | None = discord.utils.find(  # type: ignore
            lambda activity: isinstance(activity, discord.Spotify), member.activities
        )

        if not spotify:
            return await ctx.send("❌ | no spotify activity found")

        headers = {"Authorization": f"Bearer {config.JEYY_API_TOKEN}"}
        parameters = {
            "title": spotify.title,
            "cover_url": spotify.album_cover_url,
            "duration_seconds": spotify.duration.seconds,
            "start_timestamp": spotify.start.timestamp(),
            "artists": spotify.artists,
        }

        request = await self.bot.session.get("https://api.jeyy.xyz/v2/discord/spotify", parameters=parameters, headers=headers)
        bytes = BytesIO(await request.read())
        file = discord.File(bytes, "spotify.png")

        return await ctx.send(f"<:spotify:1169757922532794368> **{member.display_name}** is listening to **{spotify.title}**", file=file)
