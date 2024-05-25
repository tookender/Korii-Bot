import discord
from discord import app_commands
from discord.ext import commands

from utils import Embed

from ._base import EconomyBase
from .utils import *


class BasicCog(EconomyBase):
    @commands.hybrid_command(description="Create an account for Korii Economy")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def register(self, ctx):
        if await has_account(self.bot, ctx.author.id):
            return await self.send_embed(
                ctx,
                text=f"{self.bot.E['no']} | You already have an account registered.",
                color=discord.Color.red(),
            )

        await create_account(self.bot, ctx.author.id)
        prefix = await self.get_prefix(ctx)

        return await self.send_embed(
            ctx,
            text=f"{self.bot.E['yes']} | Successfully created an account for Korii Economy.\n" f"Use `{prefix}balance` to view your balance.",
            color=discord.Color.green(),
        )

    @commands.hybrid_command(description="View your or a user's balance.", aliases=["bal"])
    @app_commands.describe(user="The user you want to view the balance of. Defaults to yourself..")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def balance(self, ctx, user: discord.Member | None = None):
        user = user if user else ctx.author

        if await self.check_account(ctx, user):
            return

        balance = await get_balance(self.bot, user.id)
        bank = await get_bank(self.bot, user.id)

        return await self.send_embed(
            ctx,
            text=f"💵 **Money:** {balance}\n" f"🏦 **Bank:** {bank}\n" f"💰 **Total:** {balance + bank}",
            author=user,
        )

    @commands.hybrid_command(description="Give a person an amount of money.")
    @app_commands.describe(user="The user you want to give the money to.")
    @app_commands.describe(amount="The amount of money you want to give the user.")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def give(self, ctx, user: discord.Member, amount: BalanceConverter):
        if await self.check_account(ctx, user):
            return

        if not await has_enough_money(self.bot, ctx.author.id, amount):
            balance = await get_balance(self.bot, ctx.author.id)

            return await self.send_embed(
                ctx,
                text=f"{self.bot.E['no']} | You only have **${balance}**.",
                color=discord.Color.red(),
            )

        balance = await get_balance(self.bot, ctx.author.id)
        user_balance = await get_balance(self.bot, user.id)

        await remove_money(self.bot, ctx.author.id, amount)
        await add_money(self.bot, user.id, amount)

        embed = await self.send_embed(
            ctx,
            text=f"{self.bot.E['yes']} You have given **${amount}** to {user.mention}.",
            return_embed=True,
        )

        embed.add_field(name="Your balance", value=f"${balance} -> ${balance - amount}", title=False)
        embed.add_field(name=f"{user.display_name}'s balance", value=f"${user_balance} -> ${user_balance + amount}", title=False)

        return await ctx.send(embed=embed)

    @commands.hybrid_command(description="View the people with the most money.", aliases=["lb", "rank", "top"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leaderboard(self, ctx):
        users = await self.bot.pool.fetch(
            """
            SELECT user_id, balance, bank, (balance + bank) AS total_wealth
            FROM economy
            ORDER BY total_wealth DESC
            LIMIT 10
        """
        )

        leaderboard_message = []
        for i, data in enumerate(users, 1):
            user = self.bot.get_user(data["user_id"])
            leaderboard_message.append(f"**{i}.** {user.mention if user else 'N/A'} - ${data['balance'] + data['bank']}")

        embed = Embed(
            description="\n".join(leaderboard_message),
        )

        embed.set_author(
            name="Leaderboard",
            icon_url="https://media.discordapp.net/attachments/1236282958755659946/1242190293533593651/d70b9ff8f22fa25ed9c4.png",
        )

        return await ctx.send(embed=embed)
