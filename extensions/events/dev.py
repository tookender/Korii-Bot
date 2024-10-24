from discord.ext import commands
from ._base import EventsBase


class DevCog(EventsBase):
	@commands.command()
	@commands.is_owner()
	async def say(self, ctx: commands.Context, *, message: str):
		await ctx.message.delete()
		await ctx.send(message)