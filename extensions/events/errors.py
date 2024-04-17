from discord.ext import commands

from utils import Cog, BlacklistedError, Embed

errors: dict[type[Exception], str] = {
    BlacklistedError: "bro got blacklisted 💀💀 point and laugh at this user {self.bot.E['pepepoint']}",
    commands.CommandOnCooldown: "blawg calm down you on cooldown for {error.retry_after:.2f} seconds",
    commands.CheckFailure: "lil bro who told you, you can use this command ☠️",
}


class ErrorsCog(Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return

        await ctx.message.add_reaction("❌")

        if reason := errors.get(type(error)):
            embed = Embed(title="an oopsie boopsie hoopsie happened !!!!", description=reason.format(self=self, error=error))
            return await ctx.reply(embed=embed)

        embed = Embed(title="i dunno what to tell you m8", description=f"```prolog\n{error}\n```")
        return await ctx.reply(embed=embed)
