import discord
from datetime import timedelta
from discord.ext import commands

from ._base import EconomyBase, GuildContext
from .utils import add_money


class RewardsCog(EconomyBase):
    @commands.hybrid_command(description="Claim your daily reward of $1000.")
    async def daily(self, ctx: GuildContext):
        await self.claim_reward(ctx, "daily", 1000, timedelta(days=1), "You can claim your next daily reward {time}.")

    @commands.hybrid_command(description="Claim your weekly reward of $5000.")
    async def weekly(self, ctx: GuildContext):
        await self.claim_reward(ctx, "weekly", 5000, timedelta(days=7), "You can claim your next weekly reward {time}.")

    @commands.hybrid_command(description="Claim your monthly reward of $10000.")
    async def monthly(self, ctx: GuildContext):
        await self.claim_reward(ctx, "monthly", 10000, timedelta(days=31), "You can claim your next monthly reward {time}.")

    async def claim_reward(self, ctx: GuildContext, reward_type, amount, cooldown, message):
        last_claim_column = f"last_{reward_type}"
        last_claim = await self.bot.pool.fetchval(f"SELECT {last_claim_column} FROM economy WHERE user_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        now = discord.utils.utcnow()

        if last_claim is not None:
            time_since_last_claim = now - last_claim

            if time_since_last_claim < cooldown:
                next_claim_time = last_claim + cooldown
                formatted_time = discord.utils.format_dt(next_claim_time, style="R")
                await self.send_embed(ctx, text=message.format(time=formatted_time), return_embed=False)
                return

        await self.bot.pool.execute(f"UPDATE economy SET {last_claim_column} = $1 WHERE user_id = $2 AND guild_id = $3", now, ctx.author.id, ctx.guild.id)
        await add_money(self.bot, ctx.author.id, ctx.guild.id, amount)
        await self.send_embed(ctx, text=f"You've claimed your {reward_type} reward of ${amount}!", return_embed=False)
