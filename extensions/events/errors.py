from discord.ext import commands

from utils import BlacklistedError, Embed

from ._base import EventsBase

errors: dict[type[Exception], str] = {
    BlacklistedError: "bro got blacklisted 💀💀 point and laugh at this user {self.bot.E['pepepoint']}",
    commands.CommandOnCooldown: "blawg calm down you on cooldown for {error.retry_after:.2f} seconds",
    commands.CheckFailure: "lil bro who told you, you can use this command ☠️",
}


class ErrorsCog(EventsBase):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound) or (ctx.command and str(ctx.command.cog) == "Economy"):
            return

        if ctx.message:
            try:
                await ctx.message.add_reaction("❌")
            except Exception as e:
                pass

        if reason := errors.get(type(error)):
            embed = Embed(title="G-HOOOOOOST", description=reason.format(self=self, error=error))
            return await ctx.send(embed=embed)

        embed = Embed(title="something spoooky happened 👻👻", description=f"```prolog\n{error}\n```")
        return await ctx.send(embed=embed)
